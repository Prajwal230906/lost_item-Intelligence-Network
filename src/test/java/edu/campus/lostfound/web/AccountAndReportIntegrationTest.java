package edu.campus.lostfound.web;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.user;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestBuilders.formLogin;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrl;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.redirectedUrlPattern;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.hamcrest.Matchers.containsString;

import java.util.UUID;
import java.time.LocalDate;
import edu.campus.lostfound.domain.AppUser;
import edu.campus.lostfound.domain.Role;
import edu.campus.lostfound.repository.UserRepository;
import edu.campus.lostfound.repository.MatchRepository;
import edu.campus.lostfound.repository.ItemClaimRepository;
import edu.campus.lostfound.repository.ReportRepository;
import edu.campus.lostfound.repository.AuditEventRepository;
import edu.campus.lostfound.repository.NotificationRepository;
import edu.campus.lostfound.service.ReportService;
import edu.campus.lostfound.service.ClaimService;
import edu.campus.lostfound.domain.ClaimStatus;
import edu.campus.lostfound.domain.ReportType;
import edu.campus.lostfound.domain.ReportStatus;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.security.crypto.password.PasswordEncoder;

@SpringBootTest
@AutoConfigureMockMvc
class AccountAndReportIntegrationTest {
    @Autowired private MockMvc mvc;
    @Autowired private UserRepository users;
    @Autowired private PasswordEncoder passwordEncoder;
    @Autowired private ReportService reports;
    @Autowired private ClaimService claimService;
    @Autowired private MatchRepository matches;
    @Autowired private ReportRepository reportRepository;
    @Autowired private ItemClaimRepository claimRepository;
    @Autowired private AuditEventRepository auditEvents;
    @Autowired private NotificationRepository notifications;

    @Test
    void loginPageRendersCsrfTokenForSecurityProtectedForm() throws Exception {
        mvc.perform(get("/login"))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("name=\"_csrf\"")));
    }

    @Test
    void registeredUserCanSignInAndCreateAReport() throws Exception {
        String email = "user-" + UUID.randomUUID() + "@example.org";
        String password = "CampusFind!2026";
        mvc.perform(post("/register").with(csrf())
                .param("name", "Campus Tester")
                .param("email", email)
                .param("password", password))
            .andExpect(status().is3xxRedirection())
            .andExpect(redirectedUrl("/login"));

        var login = mvc.perform(formLogin("/login").user(email).password(password))
            .andExpect(status().is3xxRedirection())
            .andReturn();

        mvc.perform(post("/reports").session((org.springframework.mock.web.MockHttpSession)
        login.getRequest().getSession(false)).with(csrf())
                .param("type", "LOST")
                .param("title", "Navy water bottle")
                .param("category", "Drinkware")
                .param("description", "Matte navy bottle with a silver loop")
                .param("location", "Engineering Library")
                .param("itemDate", "2026-09-20"))
            .andExpect(status().is3xxRedirection())
            .andExpect(redirectedUrlPattern("/reports/*"));
    }

    @Test
    void dashboardRendersPotentialMatchReportTitlesAfterDatabaseSessionCloses() throws Exception {
        String lostOwner = "lost-" + UUID.randomUUID() + "@example.org";
        String foundOwner = "found-" + UUID.randomUUID() + "@example.org";
        users.save(new AppUser("Lost Owner", lostOwner, passwordEncoder.encode("CampusFind!2026"), Role.USER));
        users.save(new AppUser("Found Owner", foundOwner, passwordEncoder.encode("CampusFind!2026"), Role.USER));
        LocalDate date = LocalDate.now().minusDays(1);
        reports.create(new ReportService.CreateReport(edu.campus.lostfound.domain.ReportType.LOST,
            "Blue card holder lost", "Accessories", "Blue fabric lanyard with clear badge sleeve",
            "Central Library", date, null), lostOwner);
        reports.create(new ReportService.CreateReport(edu.campus.lostfound.domain.ReportType.FOUND,
            "Blue lanyard found", "Accessories", "Blue fabric lanyard with clear badge sleeve",
            "Central Library", date, null), foundOwner);

        mvc.perform(get("/dashboard").with(user(lostOwner).roles("USER")))
            .andExpect(status().isOk())
            .andExpect(content().string(containsString("Blue card holder lost")))
            .andExpect(content().string(containsString("Blue lanyard found")))
            .andExpect(content().string(containsString("Send claim to admin")));
    }

    @Test
    void lostOwnerCanSubmitProofAndAdminCanRejectThenApproveClaim() throws Exception {
        String lostOwner = "claimant-" + UUID.randomUUID() + "@example.org";
        String foundOwner = "finder-" + UUID.randomUUID() + "@example.org";
        users.save(new AppUser("Claimant", lostOwner, passwordEncoder.encode("CampusFind!2026"), Role.USER));
        users.save(new AppUser("Finder", foundOwner, passwordEncoder.encode("CampusFind!2026"), Role.USER));
        LocalDate date = LocalDate.now().minusDays(1);
        var lost = reports.create(new ReportService.CreateReport(ReportType.LOST, "Black wallet lost", "Wallet", "Black leather wallet with initials CJ", "Central Library", date, null), lostOwner);
        var found = reports.create(new ReportService.CreateReport(ReportType.FOUND, "Black wallet found", "Accessories", "Black leather wallet found by library tables", "Central Library", date, null), foundOwner);
        var match = matches.findByLostReportOwnerIdOrFoundReportOwnerIdOrderByScoreDesc(lost.getOwner().getId(), lost.getOwner().getId())
                .stream().filter(m -> m.getLostReport().getId().equals(lost.getId()) && m.getFoundReport().getId().equals(found.getId())).findFirst().orElseThrow();

        mvc.perform(post("/matches/" + match.getId() + "/claim").with(user(foundOwner).roles("USER")).with(csrf())
                        .param("proofDetails", "I found it"))
                .andExpect(redirectedUrl("/dashboard"));
        org.junit.jupiter.api.Assertions.assertTrue(claimRepository.findByClaimantIdOrderBySubmittedAtDesc(users.findByEmailIgnoreCase(foundOwner).orElseThrow().getId()).isEmpty());
        var firstClaim = claimService.submit(match.getId(), lostOwner, "My initials CJ are embossed inside the wallet.");
        mvc.perform(get("/admin").with(user("test-admin@example.org").roles("ADMIN")))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("My initials CJ are embossed inside the wallet.")));
        mvc.perform(post("/admin/claims/" + firstClaim.getId() + "/review").with(user("test-admin@example.org").roles("ADMIN")).with(csrf())
                        .param("decision", "REJECTED").param("adminNote", "Please provide a purchase record."))
                .andExpect(status().is3xxRedirection());
        org.junit.jupiter.api.Assertions.assertEquals(ClaimStatus.REJECTED, claimRepository.findById(firstClaim.getId()).orElseThrow().getStatus());
        org.junit.jupiter.api.Assertions.assertEquals(ReportStatus.OPEN, reportRepository.findById(lost.getId()).orElseThrow().getStatus());

        var resubmitted = claimService.submit(match.getId(), lostOwner, "Purchase receipt and initials CJ inside the wallet.");
        mvc.perform(post("/admin/claims/" + resubmitted.getId() + "/review").with(user("test-admin@example.org").roles("ADMIN")).with(csrf())
                        .param("decision", "APPROVED").param("adminNote", "Proof verified."))
                .andExpect(status().is3xxRedirection());
        org.junit.jupiter.api.Assertions.assertEquals(ClaimStatus.APPROVED, claimRepository.findById(resubmitted.getId()).orElseThrow().getStatus());
        org.junit.jupiter.api.Assertions.assertEquals(ReportStatus.RESOLVED, reportRepository.findById(lost.getId()).orElseThrow().getStatus());
        org.junit.jupiter.api.Assertions.assertEquals(ReportStatus.RESOLVED, reportRepository.findById(found.getId()).orElseThrow().getStatus());
        org.junit.jupiter.api.Assertions.assertEquals(2L, auditEvents.findAll().stream().filter(e -> "CLAIM".equals(e.getTargetType()) && (e.getTargetId().equals(firstClaim.getId()) || e.getTargetId().equals(resubmitted.getId()))).count());
        org.junit.jupiter.api.Assertions.assertTrue(notifications.findTop30ByUserIdOrderByCreatedAtDesc(users.findByEmailIgnoreCase(lostOwner).orElseThrow().getId()).stream().anyMatch(n -> n.getMessage().contains("claim was approved")));
        mvc.perform(get("/admin").with(user(lostOwner).roles("USER"))).andExpect(status().isForbidden());
    }

    @Test
    void healthEndpointIsPublicAndAdminPagesRequireAnAdministrator() throws Exception {
        mvc.perform(get("/api/health")).andExpect(status().isOk());
        mvc.perform(get("/admin")).andExpect(status().is3xxRedirection());
    }

    @Test
    void invalidRegistrationRemainsOnTheForm() throws Exception {
        mvc.perform(post("/register").with(csrf())
                .param("name", "")
                .param("email", "not-an-email")
                .param("password", "short"))
            .andExpect(status().isOk());
    }
}

