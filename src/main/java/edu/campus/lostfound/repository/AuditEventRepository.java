package edu.campus.lostfound.repository;
import edu.campus.lostfound.domain.AuditEvent;import org.springframework.data.jpa.repository.JpaRepository;
public interface AuditEventRepository extends JpaRepository<AuditEvent,Long>{}
