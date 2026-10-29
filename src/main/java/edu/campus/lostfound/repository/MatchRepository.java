package edu.campus.lostfound.repository;
import edu.campus.lostfound.domain.PotentialMatch;
import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
public interface MatchRepository extends JpaRepository<PotentialMatch,Long>{
 boolean existsByLostReportIdAndFoundReportId(Long lostId,Long foundId);
 @EntityGraph(attributePaths={"lostReport","foundReport"})
 List<PotentialMatch> findByLostReportOwnerIdOrFoundReportOwnerIdOrderByScoreDesc(Long lostOwnerId,Long foundOwnerId);
 @EntityGraph(attributePaths={"lostReport","foundReport"})
 List<PotentialMatch> findAllByOrderByScoreDesc();
}
