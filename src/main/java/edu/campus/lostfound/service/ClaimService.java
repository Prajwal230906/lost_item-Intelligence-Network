package edu.campus.lostfound.service;

import edu.campus.lostfound.domain.*;
import edu.campus.lostfound.repository.*;
import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ClaimService {
    private final ItemClaimRepository claims;
    private final MatchRepository matches;
    private final UserRepository users;
    private final AuditEventRepository audit;
    private final NotificationRepository notifications;

    public ClaimService(ItemClaimRepository claims, MatchRepository matches, UserRepository users,
                        AuditEventRepository audit, NotificationRepository notifications) {
        this.claims = claims;
        this.matches = matches;
        this.users = users;
        this.audit = audit;
        this.notifications = notifications;
    }

    @Transactional(readOnly = true)
    public List<ItemClaim> mine(String email) {
        AppUser claimant = users.findByEmailIgnoreCase(email).orElseThrow();
        return claims.findByClaimantIdOrderBySubmittedAtDesc(claimant.getId());
    }

    @Transactional
    public ItemClaim submit(Long matchId, String claimantEmail, String proofDetails) {
        String details = proofDetails == null ? "" : proofDetails.trim();
        if (details.isBlank() || details.length() > 2000) {
            throw new IllegalArgumentException("Proof details are required and must be at most 2000 characters");
        }
        PotentialMatch match = matches.findById(matchId).orElseThrow();
        AppUser claimant = users.findByEmailIgnoreCase(claimantEmail).orElseThrow();
        if (!match.getLostReport().getOwner().getId().equals(claimant.getId())) {
            throw new IllegalArgumentException("Only the owner of the lost report can submit this claim");
        }
        if (match.getLostReport().getStatus() != ReportStatus.OPEN
                || match.getFoundReport().getStatus() != ReportStatus.OPEN) {
            throw new IllegalArgumentException("This item is no longer available to claim");
        }
        if (claims.existsByMatchIdAndStatus(matchId, ClaimStatus.PENDING)) {
            throw new IllegalArgumentException("A claim for this match is already awaiting review");
        }
        return claims.save(new ItemClaim(match, claimant, details));
    }

    @Transactional(readOnly = true)
    public List<ItemClaim> pendingClaims() {
        return claims.findByStatusOrderBySubmittedAtDesc(ClaimStatus.PENDING);
    }

    @Transactional
    public ItemClaim review(Long claimId, ClaimStatus decision, String adminEmail, String note) {
        if (decision == ClaimStatus.PENDING) throw new IllegalArgumentException("Choose approve or reject");
        ItemClaim claim = claims.findById(claimId).orElseThrow();
        AppUser reviewer = users.findByEmailIgnoreCase(adminEmail).orElseThrow();
        String normalizedNote = note == null ? "" : note.trim();
        if (normalizedNote.length() > 500) throw new IllegalArgumentException("Admin note must be at most 500 characters");
        if (decision == ClaimStatus.APPROVED
                && claims.existsByMatch_FoundReport_IdAndStatusAndIdNot(claim.getMatch().getFoundReport().getId(), ClaimStatus.APPROVED, claimId)) {
            throw new IllegalArgumentException("A claim for this found item has already been approved");
        }
        claim.review(decision, reviewer, normalizedNote.isBlank() ? null : normalizedNote);
        if (decision == ClaimStatus.APPROVED) {
            claim.getMatch().getLostReport().setStatus(ReportStatus.RESOLVED);
            claim.getMatch().getFoundReport().setStatus(ReportStatus.RESOLVED);
        }
        audit.save(new AuditEvent(reviewer, "CLAIM_" + decision, "CLAIM", claim.getId()));
        notifications.save(new Notification(claim.getClaimant(), claim.getMatch(),
                decision == ClaimStatus.APPROVED
                        ? "Your item claim was approved. Contact campus administration to arrange collection."
                        : "Your item claim was not approved. Check the administrator's note or contact campus administration."));
        return claim;
    }
}
