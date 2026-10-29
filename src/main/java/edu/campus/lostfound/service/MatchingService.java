package edu.campus.lostfound.service;

import edu.campus.lostfound.domain.*;
import edu.campus.lostfound.repository.*;
import java.text.Normalizer;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class MatchingService {
    private final ReportRepository reports; private final MatchRepository matches; private final NotificationRepository notifications;
    private final double categoryWeight,descriptionWeight,locationWeight,dateWeight,threshold; private final int dateWindow;
    public MatchingService(ReportRepository reports,MatchRepository matches,NotificationRepository notifications,
      @Value("${app.matching.category-weight:0.25}") double categoryWeight,
      @Value("${app.matching.description-weight:0.35}") double descriptionWeight,
      @Value("${app.matching.location-weight:0.25}") double locationWeight,
      @Value("${app.matching.date-weight:0.15}") double dateWeight,
      @Value("${app.matching.threshold:0.55}") double threshold,
      @Value("${app.matching.date-window-days:30}") int dateWindow){
      this.reports=reports;this.matches=matches;this.notifications=notifications;this.categoryWeight=categoryWeight;this.descriptionWeight=descriptionWeight;this.locationWeight=locationWeight;this.dateWeight=dateWeight;this.threshold=threshold;this.dateWindow=dateWindow;
      if(Math.abs(categoryWeight+descriptionWeight+locationWeight+dateWeight-1.0)>0.0001||categoryWeight<0||descriptionWeight<0||locationWeight<0||dateWeight<0||categoryWeight>1||descriptionWeight>1||locationWeight>1||dateWeight>1||threshold<0||threshold>1||dateWindow<1) throw new IllegalArgumentException("Matching weights must be between 0 and 1 and sum to one; threshold must be 0..1 and date window positive");
    }
    @Transactional public void process(ItemReport report){
      if(report.getStatus()!=ReportStatus.OPEN)return;
      ReportType opposite=report.getType()==ReportType.LOST?ReportType.FOUND:ReportType.LOST;
      for(ItemReport candidate:reports.findByTypeAndStatusOrderByCreatedAtDesc(opposite,ReportStatus.OPEN)){
        ItemReport lost=report.getType()==ReportType.LOST?report:candidate, found=report.getType()==ReportType.FOUND?report:candidate;
        if(matches.existsByLostReportIdAndFoundReportId(lost.getId(),found.getId()))continue;
        Result result=score(lost,found);
        if(result.score()/100.0>=threshold){
          PotentialMatch match=matches.save(new PotentialMatch(lost,found,result.score(),result.categoryScore(),result.descriptionScore(),result.locationScore(),result.dateTimeScore(),result.explanation()));
          notifications.save(new Notification(lost.getOwner(),match,"A possible found-item match is ready for review."));
          notifications.save(new Notification(found.getOwner(),match,"A possible lost-item match is ready for review."));
        }
      }
    }
    public Result score(ItemReport lost,ItemReport found){
      double category=categorySimilarity(lost.getCategory(),found.getCategory());
      Set<String> titleTokens=tokens(lost.getTitle()),foundTitleTokens=tokens(found.getTitle());
      Set<String> a=tokens(lost.getDescription()),b=tokens(found.getDescription());
      double titleSimilarity=tokenSimilarity(titleTokens,foundTitleTokens);
      double bodySimilarity=tokenSimilarity(a,b);
      // Titles often contain the clearest item identity while descriptions vary by reporter.
      double description=.40*titleSimilarity+.60*bodySimilarity;
      Set<String> intersection=new HashSet<>(a);intersection.retainAll(b);
      double location=locationSimilarity(lost.getLocation(),found.getLocation());
      long days=Math.abs(ChronoUnit.DAYS.between(lost.getItemDate(),found.getItemDate()));
      double dateScore=days>dateWindow?0:100.0*(1.0-(double)days/dateWindow);
      double dateTime=dateScore;
      String timeDetail="time not supplied; date score used";
      if(lost.getItemTime()!=null&&found.getItemTime()!=null){
        long minuteDelta=Math.abs(ChronoUnit.MINUTES.between(lost.getItemTime(),found.getItemTime()));
        minuteDelta=Math.min(minuteDelta,1440-minuteDelta);
        timeDetail=minuteDelta+" minute(s) apart";
        if(days<=dateWindow){
          double timeScore=Math.max(0,100.0*(1.0-(double)minuteDelta/720.0));
          dateTime=.70*dateScore+.30*timeScore;
        }else dateTime=0;
      }
      double total=(category*categoryWeight+description*descriptionWeight+location*locationWeight+dateTime*dateWeight);
      total=Math.max(0,Math.min(100,total));
      String categoryDetail=category>0?canonicalCategory(lost.getCategory())+" category matches":"categories differ";
      List<String> shared=intersection.stream().sorted().limit(5).toList();
      String descriptionDetail=String.format(Locale.ROOT,"title %.0f/100, description %.0f/100%s",titleSimilarity,bodySimilarity,shared.isEmpty()?"; no shared description keywords":"; shared keywords: "+String.join(", ",shared));
      String locationDetail=location==100?"locations match exactly":location>0?"one location contains the other":"locations differ";
      String explanation=String.format(Locale.ROOT,"Category %.0f/100 (%s); description %.0f/100 (%s); location %.0f/100 (%s); date/time %.0f/100 (%d day(s), %s).",category,categoryDetail,description,descriptionDetail,location,locationDetail,dateTime,days,timeDetail);
      return new Result(Math.round(total*100.0)/100.0,Math.round(category*100.0)/100.0,Math.round(description*100.0)/100.0,Math.round(location*100.0)/100.0,Math.round(dateTime*100.0)/100.0,explanation);
    }
    private static double categorySimilarity(String x,String y){return canonicalCategory(x).equals(canonicalCategory(y))?100:0;}
    private static String canonicalCategory(String value){String v=normalized(value);return switch(v){case "phone","mobile","cell phone","mobile phone","laptop","computer","tablet"->"electronics";case "wallet","purse","keychain"->"accessories";case "backpack","rucksack","handbag"->"bags";default->v;};}
    private static double locationSimilarity(String x,String y){String a=normalized(x),b=normalized(y);if(a.equals(b))return 100;if(a.contains(b)||b.contains(a))return 75;return tokenSimilarity(tokens(a),tokens(b));}
    private static double tokenSimilarity(Set<String> a,Set<String> b){if(a.isEmpty()||b.isEmpty())return 0;Set<String> intersection=new HashSet<>(a);intersection.retainAll(b);return 200.0*intersection.size()/(a.size()+b.size());}
    private static Set<String> tokens(String value){return Arrays.stream(normalized(value).split("\\W+")).filter(s->s.length()>1).collect(Collectors.toSet());}
    private static String normalized(String value){return Normalizer.normalize(value==null?"":value,Normalizer.Form.NFD).replaceAll("\\p{M}","").toLowerCase(Locale.ROOT).trim().replaceAll("\\s+"," ");}
    public record Result(double score,double categoryScore,double descriptionScore,double locationScore,double dateTimeScore,String explanation){}
}
