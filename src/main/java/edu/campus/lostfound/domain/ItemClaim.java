package edu.campus.lostfound.domain;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "item_claims", indexes = {@Index(name = "idx_item_claim_status", columnList = "status,submitted_at"), @Index(name = "idx_item_claim_match", columnList = "match_id,status")})
public class ItemClaim {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false, fetch = FetchType.LAZY) @JoinColumn(name = "match_id")
    private PotentialMatch match;

    @ManyToOne(optional = false, fetch = FetchType.LAZY) @JoinColumn(name = "claimant_id")
    private AppUser claimant;

    @Column(name = "proof_details", nullable = false, length = 2000)
    private String proofDetails;

    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20)
    private ClaimStatus status = ClaimStatus.PENDING;

    @ManyToOne(fetch = FetchType.LAZY) @JoinColumn(name = "reviewer_id")
    private AppUser reviewer;

    @Column(name = "admin_note", length = 500)
    private String adminNote;

    @Column(name = "submitted_at", nullable = false)
    private Instant submittedAt = Instant.now();

    @Column(name = "reviewed_at")
    private Instant reviewedAt;

    protected ItemClaim() { }

    public ItemClaim(PotentialMatch match, AppUser claimant, String proofDetails) {
        this.match = match;
        this.claimant = claimant;
        this.proofDetails = proofDetails;
    }

    public void review(ClaimStatus decision, AppUser reviewer, String note) {
        if (status != ClaimStatus.PENDING) throw new IllegalStateException("This claim has already been reviewed");
        if (decision == ClaimStatus.PENDING) throw new IllegalArgumentException("A review decision is required");
        this.status = decision;
        this.reviewer = reviewer;
        this.adminNote = note;
        this.reviewedAt = Instant.now();
    }

    public Long getId() { return id; }
    public PotentialMatch getMatch() { return match; }
    public AppUser getClaimant() { return claimant; }
    public String getProofDetails() { return proofDetails; }
    public ClaimStatus getStatus() { return status; }
    public AppUser getReviewer() { return reviewer; }
    public String getAdminNote() { return adminNote; }
    public Instant getSubmittedAt() { return submittedAt; }
    public Instant getReviewedAt() { return reviewedAt; }
}
