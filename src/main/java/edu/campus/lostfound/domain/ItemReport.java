package edu.campus.lostfound.domain;

import jakarta.persistence.*;
import java.time.Instant;
import java.time.LocalDate;import java.time.LocalTime;

@Entity @Table(name="item_reports", indexes={@Index(name="idx_report_type_status",columnList="type,status"),@Index(name="idx_report_category",columnList="category"),@Index(name="idx_report_date",columnList="item_date")})
public class ItemReport {
    @Id @GeneratedValue(strategy=GenerationType.IDENTITY) private Long id;
    @Enumerated(EnumType.STRING) @Column(nullable=false,length=12) private ReportType type;
    @Column(nullable=false,length=80) private String title;
    @Column(nullable=false,length=40) private String category;
    @Column(nullable=false,length=2000) private String description;
    @Column(nullable=false,length=120) private String location;
    @Column(name="item_date",nullable=false) private LocalDate itemDate;
    @Column(name="item_time") private LocalTime itemTime;
    @Enumerated(EnumType.STRING) @Column(nullable=false,length=20) private ReportStatus status=ReportStatus.OPEN;
    @ManyToOne(fetch=FetchType.LAZY,optional=false) @JoinColumn(name="owner_id") private AppUser owner;
    @Column(nullable=false) private Instant createdAt=Instant.now();
    @Column(nullable=false) private Instant updatedAt=Instant.now();
    protected ItemReport() { }
    public ItemReport(ReportType type,String title,String category,String description,String location,LocalDate itemDate,LocalTime itemTime,AppUser owner){this.type=type;this.title=title;this.category=category;this.description=description;this.location=location;this.itemDate=itemDate;this.itemTime=itemTime;this.owner=owner;}
    @PreUpdate void touch(){updatedAt=Instant.now();}
    public Long getId(){return id;} public ReportType getType(){return type;} public String getTitle(){return title;} public String getCategory(){return category;} public String getDescription(){return description;} public String getLocation(){return location;} public LocalDate getItemDate(){return itemDate;} public LocalTime getItemTime(){return itemTime;} public ReportStatus getStatus(){return status;} public AppUser getOwner(){return owner;} public Instant getCreatedAt(){return createdAt;}
    public void setStatus(ReportStatus status){this.status=status;}
}
