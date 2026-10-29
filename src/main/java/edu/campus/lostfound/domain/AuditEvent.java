package edu.campus.lostfound.domain;
import jakarta.persistence.*;import java.time.Instant;
@Entity @Table(name="audit_events",indexes={@Index(name="idx_audit_target",columnList="target_type,target_id"),@Index(name="idx_audit_actor",columnList="actor_id,occurred_at")})
public class AuditEvent{
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY)private Long id;
 @ManyToOne(optional=false,fetch=FetchType.LAZY)@JoinColumn(name="actor_id")private AppUser actor;
 @Column(nullable=false,length=60)private String action;
 @Column(name="target_type",nullable=false,length=40)private String targetType;
 @Column(name="target_id",nullable=false)private Long targetId;
 @Column(name="occurred_at",nullable=false)private Instant occurredAt=Instant.now();
 protected AuditEvent(){}
 public AuditEvent(AppUser actor,String action,String targetType,Long targetId){this.actor=actor;this.action=action;this.targetType=targetType;this.targetId=targetId;}
 public Long getId(){return id;}public String getAction(){return action;}public String getTargetType(){return targetType;}public Long getTargetId(){return targetId;}public Instant getOccurredAt(){return occurredAt;}
}
