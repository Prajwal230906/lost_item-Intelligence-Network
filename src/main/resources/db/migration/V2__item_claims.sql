CREATE TABLE item_claims (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 match_id BIGINT NOT NULL,
 claimant_id BIGINT NOT NULL,
 proof_details VARCHAR(2000) NOT NULL,
 status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
 reviewer_id BIGINT NULL,
 admin_note VARCHAR(500) NULL,
 submitted_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 reviewed_at TIMESTAMP(6) NULL,
 CONSTRAINT fk_claim_match FOREIGN KEY(match_id) REFERENCES potential_matches(id),
 CONSTRAINT fk_claim_claimant FOREIGN KEY(claimant_id) REFERENCES app_users(id),
 CONSTRAINT fk_claim_reviewer FOREIGN KEY(reviewer_id) REFERENCES app_users(id),
 INDEX idx_item_claim_status(status,submitted_at),
 INDEX idx_item_claim_match(match_id,status)
);
