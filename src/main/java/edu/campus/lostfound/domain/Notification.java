package edu.campus.lostfound.domain;
import jakarta.persistence.*;import java.time.Instant;
@Entity @Table(name="notifications",indexes=@Index(name="idx_notification_user_read",columnList="user_id,read_at"))
public class Notification{
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY)private Long id;
 @ManyToOne(optional=false,fetch=FetchType.LAZY)@JoinColumn(name="user_id")private AppUser user;
 @ManyToOne(fetch=FetchType.LAZY)@JoinColumn(name="match_id")private PotentialMatch match;
 @Column(nullable=false,length=240)private String message;
 @Column(nullable=false)private Instant createdAt=Instant.now();
 @Column(name="read_at")private Instant readAt;
 protected Notification(){}
 public Notification(AppUser user,PotentialMatch match,String message){this.user=user;this.match=match;this.message=message;}
 public Long getId(){return id;}public String getMessage(){return message;}public Instant getCreatedAt(){return createdAt;}public Instant getReadAt(){return readAt;}public void markRead(){if(readAt==null)readAt=Instant.now();}
}
