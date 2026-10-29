package edu.campus.lostfound.repository;
import edu.campus.lostfound.domain.*;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
public interface ReportRepository extends JpaRepository<ItemReport,Long>{
 List<ItemReport> findByStatusOrderByCreatedAtDesc(ReportStatus status);
 List<ItemReport> findByTypeAndStatusOrderByCreatedAtDesc(ReportType type,ReportStatus status);
 List<ItemReport> findByOwnerIdOrderByCreatedAtDesc(Long ownerId);
}
