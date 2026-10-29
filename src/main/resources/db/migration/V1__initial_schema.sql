CREATE TABLE app_users (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(190) NOT NULL UNIQUE,
 password_hash VARCHAR(100) NOT NULL,
 role VARCHAR(20) NOT NULL,
 created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);
CREATE TABLE item_reports (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 type VARCHAR(12) NOT NULL,
 title VARCHAR(80) NOT NULL,
 category VARCHAR(40) NOT NULL,
 description VARCHAR(2000) NOT NULL,
 location VARCHAR(120) NOT NULL,
 item_date DATE NOT NULL,
 item_time TIME NULL,
 status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
 owner_id BIGINT NOT NULL,
 created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 updated_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 CONSTRAINT fk_report_owner FOREIGN KEY(owner_id) REFERENCES app_users(id),
 INDEX idx_report_type_status(type,status),
 INDEX idx_report_category(category),
 INDEX idx_report_date(item_date)
);
CREATE TABLE potential_matches (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 lost_report_id BIGINT NOT NULL,
 found_report_id BIGINT NOT NULL,
 score DOUBLE NOT NULL,
 category_score DOUBLE NOT NULL,
 description_score DOUBLE NOT NULL,
 location_score DOUBLE NOT NULL,
 date_time_score DOUBLE NOT NULL,
 explanation VARCHAR(1000) NOT NULL,
 review_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
 created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 CONSTRAINT fk_match_lost FOREIGN KEY(lost_report_id) REFERENCES item_reports(id),
 CONSTRAINT fk_match_found FOREIGN KEY(found_report_id) REFERENCES item_reports(id),
 CONSTRAINT uq_match_pair UNIQUE(lost_report_id,found_report_id),
 INDEX idx_match_review(review_status,score)
);
CREATE TABLE notifications (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 user_id BIGINT NOT NULL,
 match_id BIGINT NULL,
 message VARCHAR(240) NOT NULL,
 created_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 read_at TIMESTAMP(6) NULL,
 CONSTRAINT fk_notification_user FOREIGN KEY(user_id) REFERENCES app_users(id),
 CONSTRAINT fk_notification_match FOREIGN KEY(match_id) REFERENCES potential_matches(id),
 INDEX idx_notification_user_read(user_id,read_at)
);
CREATE TABLE audit_events (
 id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 actor_id BIGINT NOT NULL,
 action VARCHAR(60) NOT NULL,
 target_type VARCHAR(40) NOT NULL,
 target_id BIGINT NOT NULL,
 occurred_at TIMESTAMP(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
 CONSTRAINT fk_audit_actor FOREIGN KEY(actor_id) REFERENCES app_users(id),
 INDEX idx_audit_target(target_type,target_id),
 INDEX idx_audit_actor(actor_id,occurred_at)
);
