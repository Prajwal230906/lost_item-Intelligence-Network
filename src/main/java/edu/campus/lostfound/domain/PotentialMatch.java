package edu.campus.lostfound.domain;

import jakarta.persistence.*;
import java.time.Instant;

@Entity @Table(name="potential_matches", uniqueConstraints=@UniqueConstraint(name="uq_match_pair",columnNames={"lost_report_id","found_report_id"}),indexes=@Index(name="idx_match_review",columnList="review_status,score"))
public class PotentialMatch {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @ManyToOne(optional=false,fetch=FetchType.LAZY) @JoinColumn(name="lost_report_id") private ItemReport lostReport;
    @ManyToOne(optional=false,fetch=FetchType.LAZY) @JoinColumn(name="found_report_id") private ItemReport foundReport;
    @Column(nullable=false) private double score;
    @Column(name="category_score",nullable=false) private double categoryScore;
    @Column(name="description_score",nullable=false) private double descriptionScore;
    @Column(name="location_score",nullable=false) private double locationScore;
    @Column(name="date_time_score",nullable=false) private double dateTimeScore;
    @Column(nullable=false,length=1000) private String explanation;
    @Column(name="review_status",nullable=false,length=20) private String reviewStatus="PENDING";
    @Column(nullable=false) private Instant createdAt=Instant.now();
    protected PotentialMatch() { }
    public PotentialMatch(ItemReport lost,ItemReport found,double score,double categoryScore,double descriptionScore,double locationScore,double dateTimeScore,String explanation){this.lostReport=lost;this.foundReport=found;this.score=score;this.categoryScore=categoryScore;this.descriptionScore=descriptionScore;this.locationScore=locationScore;this.dateTimeScore=dateTimeScore;this.explanation=explanation;}
    public Long getId(){return id;} public ItemReport getLostReport(){return lostReport;} public ItemReport getFoundReport(){return foundReport;} public double getScore(){return score;} public double getCategoryScore(){return categoryScore;} public double getDescriptionScore(){return descriptionScore;} public double getLocationScore(){return locationScore;} public double getDateTimeScore(){return dateTimeScore;} public String getExplanation(){return explanation;} public String getReviewStatus(){return reviewStatus;}
    public void review(String value){this.reviewStatus=value;}
}
