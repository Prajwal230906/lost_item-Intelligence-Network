package edu.campus.lostfound.repository;
import edu.campus.lostfound.domain.Notification;import java.util.List;import java.util.Optional;import org.springframework.data.jpa.repository.JpaRepository;
public interface NotificationRepository extends JpaRepository<Notification,Long>{List<Notification> findTop30ByUserIdOrderByCreatedAtDesc(Long userId);Optional<Notification> findByIdAndUserId(Long id,Long userId);}
