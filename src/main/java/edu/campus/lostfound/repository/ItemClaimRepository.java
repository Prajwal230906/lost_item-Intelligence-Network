package edu.campus.lostfound.repository;

import edu.campus.lostfound.domain.ItemClaim;
import java.util.List;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemClaimRepository extends JpaRepository<ItemClaim, Long> {
    @EntityGraph(attributePaths = {"match", "match.lostReport", "match.foundReport"})
    List<ItemClaim> findByClaimantIdOrderBySubmittedAtDesc(Long claimantId);

    @EntityGraph(attributePaths = {"match", "match.lostReport", "match.foundReport", "claimant", "reviewer"})
    List<ItemClaim> findAllByOrderBySubmittedAtDesc();

    @EntityGraph(attributePaths = {"match", "match.lostReport", "match.foundReport", "claimant", "reviewer"})
    List<ItemClaim> findByStatusOrderBySubmittedAtDesc(edu.campus.lostfound.domain.ClaimStatus status);

    boolean existsByMatchIdAndStatus(Long matchId, edu.campus.lostfound.domain.ClaimStatus status);

    boolean existsByMatch_FoundReport_IdAndStatusAndIdNot(Long foundReportId, edu.campus.lostfound.domain.ClaimStatus status, Long claimId);
}
