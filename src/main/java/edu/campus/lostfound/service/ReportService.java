package edu.campus.lostfound.service;

import edu.campus.lostfound.domain.*;import edu.campus.lostfound.repository.*;
import jakarta.validation.constraints.*;import java.time.LocalDate;import java.time.LocalTime;import java.util.List;
import org.springframework.stereotype.Service;import org.springframework.transaction.annotation.Transactional;

@Service public class ReportService{
 private final ReportRepository reports;private final UserRepository users;private final MatchingService matching;
 public ReportService(ReportRepository reports,UserRepository users,MatchingService matching){this.reports=reports;this.users=users;this.matching=matching;}
 @Transactional public ItemReport create(CreateReport input,String email){AppUser owner=users.findByEmailIgnoreCase(email).orElseThrow();ItemReport saved=reports.save(new ItemReport(input.type(),input.title().trim(),input.category().trim(),input.description().trim(),input.location().trim(),input.itemDate(),input.itemTime(),owner));matching.process(saved);return saved;}
 @Transactional(readOnly=true) public List<ItemReport> search(String q,ReportType type){String term=q==null?"":q.toLowerCase();return reports.findByStatusOrderByCreatedAtDesc(ReportStatus.OPEN).stream().filter(r->type==null||r.getType()==type).filter(r->term.isBlank()||(r.getTitle()+" "+r.getDescription()+" "+r.getCategory()+" "+r.getLocation()).toLowerCase().contains(term)).toList();}
 @Transactional(readOnly=true) public List<ItemReport> mine(String email){AppUser owner=users.findByEmailIgnoreCase(email).orElseThrow();return reports.findByOwnerIdOrderByCreatedAtDesc(owner.getId());}
 public record CreateReport(@NotNull ReportType type,@NotBlank @Size(max=80) String title,@NotBlank @Size(max=40) String category,@NotBlank @Size(max=2000) String description,@NotBlank @Size(max=120) String location,@NotNull @PastOrPresent LocalDate itemDate,LocalTime itemTime){}
}
