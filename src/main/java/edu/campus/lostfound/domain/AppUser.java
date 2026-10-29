package edu.campus.lostfound.domain;

import jakarta.persistence.*;
import java.time.Instant;

@Entity @Table(name = "app_users")
public class AppUser {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @Column(nullable = false, length = 100) private String name;
    @Column(nullable = false, unique = true, length = 190) private String email;
    @Column(name = "password_hash", nullable = false) private String passwordHash;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20) private Role role = Role.USER;
    @Column(nullable = false) private Instant createdAt = Instant.now();
    protected AppUser() { }
    public AppUser(String name, String email, String passwordHash, Role role) { this.name=name; this.email=email.toLowerCase(); this.passwordHash=passwordHash; this.role=role; }
    public Long getId(){return id;} public String getName(){return name;} public String getEmail(){return email;} public String getPasswordHash(){return passwordHash;} public Role getRole(){return role;}
}
