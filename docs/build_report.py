from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/"docs"; IMG=DOCS/"images"; IMG.mkdir(parents=True,exist_ok=True); OUT=ROOT/"PROJECT_REPORT.docx"
NAVY="#142C3D"; TEAL="#16877E"; INK="#243A45"; GREY="#637780"
def font(n,b=False):
    for x in (["C:/Windows/Fonts/segoeuib.ttf","C:/Windows/Fonts/segoeui.ttf"] if b else ["C:/Windows/Fonts/segoeui.ttf","C:/Windows/Fonts/arial.ttf"]):
        if Path(x).exists(): return ImageFont.truetype(x,n)
    return ImageFont.load_default()
def diagram(name,title,boxes,links):
    w,h=1500,640; im=Image.new("RGB",(w,h),"#F7F8F5"); d=ImageDraw.Draw(im); d.text((50,35),title,font=font(34,True),fill=NAVY)
    gap=22; bw=(w-100-gap*(len(boxes)-1))//len(boxes); y=205; bh=205; ps=[]
    for i,(head,lines) in enumerate(boxes):
        x=50+i*(bw+gap); d.rounded_rectangle((x,y,x+bw,y+bh),radius=20,fill="white",outline="#D9E4DF",width=3)
        d.rounded_rectangle((x,y,x+bw,y+57),radius=20,fill=TEAL);d.rectangle((x,y+34,x+bw,y+57),fill=TEAL)
        d.text((x+15,y+12),head,font=font(22,True),fill="white")
        for j,line in enumerate(lines):d.text((x+15,y+78+j*32),line,font=font(17),fill=INK)
        ps.append((x,bw))
    for i,label in enumerate(links):
        x,b=ps[i]; nx,_=ps[i+1]; cy=y+bh//2;d.line((x+b+3,cy,nx-5,cy),fill=TEAL,width=5);d.polygon([(nx-5,cy),(nx-18,cy-10),(nx-18,cy+10)],fill=TEAL)
    d.text((50,h-50),"Design illustration, not runtime evidence",font=font(16),fill=GREY)
    q=IMG/name;im.save(q);return q
arch=diagram("architecture.png","Three-tier application architecture",[("Presentation",["Thymeleaf pages","Responsive CSS and JS","MVC and REST"]),("Application",["Security and validation","Report service","Matching workflow"]),("Data",["JPA repositories","Hibernate ORM","MySQL and Flyway"]),("Operations",["Maven verification","Jenkins pipeline","Docker Compose"])],["HTTP session","service calls","JPA"])
flow=diagram("workflow.png","Report matching and review",[("Report",["Lost or found","Campus location","Date and optional time"]),("Compare",["Category 25%","Description 35%","Location 25%"]),("Candidate",["Date/time 15%","55% threshold","Saved explanation"]),("Review",["Owner notice","Admin decision","Audit event"])],["submit","score","notify"])
db=diagram("database.png","Relational data model",[("app_users",["id and email","password hash","role"]),("item_reports",["owner key","type and status","date and time"]),("potential_matches",["lost and found ids","component scores","review status"]),("support",["notifications","audit events","foreign keys"])],["owns","candidate pairs","records"])
pipe=diagram("pipeline.png","Continuous integration path",[("GitHub",["feature branch","pull request","review"]),("Jenkins",["Maven verify","JUnit reports","SonarQube"]),("Docker",["build image","Compose stack","environment"]),("Operator",["review results","manage secrets","deploy"])],["checkout","quality","package"])
placeholder=Image.new("RGB",(1400,760),"#F7F8F5");pd=ImageDraw.Draw(placeholder)
pd.rounded_rectangle((45,45,1355,715),radius=26,fill="white",outline="#B8CDC4",width=5)
pd.rounded_rectangle((75,75,1325,180),radius=18,fill=NAVY)
pd.text((110,105),"SCREENSHOT PLACEHOLDER",font=font(35,True),fill="white")
pd.text((140,300),"Capture after local application startup",font=font(36,True),fill=TEAL)
pd.text((140,375),"Landing page  |  Report form  |  Match dashboard  |  Admin review",font=font(23),fill=INK)
pd.text((140,475),"No runtime screenshot is available in this report version.",font=font(22),fill=GREY)
placeholder_path=IMG/"screenshot-placeholder.png";placeholder.save(placeholder_path)

pages=[
("Chapter 1  Introduction","scope","Campus lost-and-found information is often split across service desks, messaging groups, notice boards, and personal networks. Someone searching one channel may not know that a similar item was reported elsewhere. A centralized service can retain structured reports and make candidates discoverable while keeping the final ownership decision with people."),
("Chapter 1  Problem context","scope","Manual comparison is slow because lost and found descriptions use different words, places have informal names, and reports may be scattered across channels. Staff also need to distinguish open reports from items already reviewed or returned. These problems motivate structured fields, search, consistent status, and a review process."),
("Chapter 1  Objectives and scope","scope","The prototype implements account registration, session sign-in, role-based administration, report creation, search, candidate matches, component explanations, owner notifications, administrative review, audit events, and responsive browser pages. It also includes tests, database migration, Maven, Jenkins, SonarQube, and Docker configuration."),
("Chapter 2  Existing process limits","scope","Informal processes have low setup cost but weak continuity. A notice board is local, a message thread is difficult to search when it grows, and multiple counters may not share status updates. Centralization improves discoverability but also creates security, retention, and operational responsibilities."),
("Chapter 2  Proposed workflow","reports","A signed-in user creates a lost or found report. The service validates and stores it, compares it with open reports of the opposite type, and saves candidate pairs above a threshold. Both owners receive an in-app notice. An administrator reviews the pair and records a decision."),
("Chapter 2  Users and permissions","security","Students, faculty, staff, security workers, and administrators are the intended user groups. Public registration creates only USER accounts. Administrators are bootstrapped from environment configuration, and protected routes require the ADMIN role. No user supplied role is accepted at registration."),
("Chapter 3  Functional requirements","api","Core functions are registration, login, report creation, report search, report retrieval, candidate retrieval, notification listing and read acknowledgment, and administrator review. Lost and found use a common report entity with a type field. REST DTOs return selected values without exposing persistence details."),
("Chapter 3  Quality requirements","data","Maintainability uses constructor injection, focused services, repository interfaces, configuration through environment variables, migrations, and tests. Explainability stores every component score. Reliability uses transaction boundaries, foreign keys, and a unique constraint on report pairs."),
("Chapter 3  Validation and privacy","security","Server validation limits names, titles, categories, descriptions, locations, emails, and passwords. Dates cannot be in the future; time is optional. Thymeleaf escapes user text, and report cards do not publish account email. Image uploads and contact-sharing features are not implemented."),
("Chapter 4  Layered architecture","data","Presentation contains Thymeleaf pages, CSS, MVC controllers, and REST routes. Application services implement account, report, matching, validation, and security behavior. Data access uses JPA repositories with MySQL and Flyway. This division keeps user interaction, business decisions, and persistence separate.","figure:arch"),
("Chapter 4  Request flow","matching","A browser submission passes through session security and CSRF protection, binding, validation, and the report service. Within a transaction the service stores the report, queries open reports of the other type, calculates scores, prevents duplicate pairs, then persists candidates and notifications.","figure:flow"),
("Chapter 4  Configuration","ops","Port, database URL, account credentials, bootstrap administrator, and matching parameters are externalized. Local development targets localhost; Compose overrides the database host. Flyway owns schema creation and Hibernate validates mappings instead of changing production tables."),
("Chapter 4  Transactions","data","Report creation, candidate persistence, and notices share transaction boundaries. A unique key prevents duplicate lost/found pairs. The normal path checks for an existing pair first. Concurrent race handling should still catch the database constraint and treat the pair as already present."),
("Chapter 5  Schema overview","data","The schema contains users, item reports, potential matches, notifications, and audit events. Reports reference owners; matches reference one lost and one found report; notices reference a user and optionally a match; audit rows reference the administrator and target.","figure:db"),
("Chapter 5  Indexes and migrations","data","Flyway migration V1 creates tables, constraints, and indexes. Hibernate uses schema validation. Indexes cover report type/status, category/date, match review, user notification retrieval, and audit lookup. Free-text search is still performed in application memory and needs database-side pagination for larger data."),
("Chapter 6  Authentication","security","Registration stores a BCrypt hash and assigns USER role. Spring Security loads accounts through a database-backed UserDetailsService. The application uses session authentication and default CSRF protection. Email verification, recovery, lockout, and institutional single sign-on are outside this prototype."),
("Chapter 6  Report lifecycle","reports","A report stores type, title, category, description, location, date, optional time, owner, status, and timestamps. New rows are OPEN. Administrators may move a report to UNDER_REVIEW, RESOLVED, or REJECTED. New matches only compare open reports."),
("Chapter 6  Search and discovery","api","Search takes text and an optional report type, then checks title, description, category, and location case-insensitively. Only open reports are returned. The homepage shows a limited sample. The current implementation has no pagination and is intended for small demonstrations."),
("Chapter 6  Candidate persistence","matching","Each candidate stores the lost and found references, weighted score, four component scores, explanation, review status, and creation time. Pair direction is consistent regardless of arrival order. A score crossing the threshold suggests review and never proves ownership."),
("Chapter 6  Notifications and audit","data","Notifications include owner, optional match, message, created time, and optional read time. The API scopes read acknowledgment to both notification id and current user. Administrator status changes and match decisions record actor, action, target, and timestamp."),
("Chapter 6  Administration","security","The review center lists open reports and candidate pairs by score. Administrators can confirm or reject a candidate and update report status. Role authorization protects write routes. The workflow lacks evidence attachments, rejection reasons, case assignment, and a formal transition graph."),
("Chapter 6  Error handling","api","JSON validation errors return field details with status 400. Invalid login uses a generic message. User text is escaped in templates, and JPA repository queries are parameterized. A complete problem-detail schema and structured request logging remain future hardening."),
("Chapter 7  Weighted model","matching","Part 7 of the pasted request specifies category 25%, description 35%, location 25%, and date/time 15%. The slide deck lists these four factors without numerical weights. The implementation follows the explicit values in the request and validates that they sum to one.","weights"),
("Chapter 7  Category and description scores","matching","Normalized exact categories score 100, as do documented synonym groups: phone and computer types map to electronics; wallet and purse map to accessories; backpack and handbag map to bags. Descriptions use Jaccard overlap after case, punctuation, and whitespace normalization."),
("Chapter 7  Location and date/time scores","matching","Normalized exact locations score 100; lexical containment scores 75; unrelated locations score zero. Date similarity falls linearly across a 30-day window. If both approximate times exist, date/time combines 70% date and 30% time-of-day score; otherwise the date score is used."),
("Chapter 7  Explanation and threshold","matching","Explanations include each component score, category comparison, up to five shared keywords, location rule, elapsed days, and time availability. The default threshold is 55% and is configurable. Owners receive a neutral notice and administrators decide whether the candidate is valid."),
("Chapter 8  Visual identity","ui","The visual system uses midnight blue, teal, off-white backgrounds, white cards, restrained borders, and a readable sans-serif hierarchy. Landing-page actions separate lost and found reporting. Recent report cards and a short process description make the service understandable at first glance."),
("Chapter 8  Forms and responsive behavior","ui","Forms use visible labels, native controls, field-level error positions, length limits, and an optional time input. Search combines text and type. Cards stack on small screens, tables scroll horizontally, and controls receive visible keyboard focus styling."),
("Chapter 8  Screenshot evidence","ui","The report contains generated architecture and data-flow illustrations, not screenshots of a running application. The source templates cover landing, sign-in, registration, report form, search, detail, dashboard, and review center. Browser inspection must happen after the app is started."),
("Chapter 9  Test strategy","tests","JUnit 5, Mockito, Spring Boot Test, MockMvc, and H2 are configured. Matching tests use mocked repositories; integration tests use an isolated in-memory database. The intended verification command runs tests and creates JaCoCo output without touching production data."),
("Chapter 9  Matching unit cases","tests","Unit tests cover exact scoring, category synonyms, partial location, Jaccard similarity, optional time, distant dates, weighted totals, score bounds, threshold rejection, duplicate suppression, notices, and invalid weights. Fixtures use synthetic campus reports."),
("Chapter 9  Integration cases","tests","MockMvc tests cover registration, sign-in, report creation, invalid registration, public health, and anonymous admin redirection. Further tests should cover found reports, search filters, notification ownership, admin review persistence, audit rows, and database uniqueness."),
("Chapter 9  Verification record","tests","The authoring environment did not expose usable Maven or Docker commands. Compilation, JUnit execution, MySQL migration, browser rendering, SonarQube, image build, and deployment remain unverified. No pass count, coverage percentage, quality gate, or live URL is claimed."),
("Chapter 10  Git workflow","ops","The guide keeps main for releases and develop for integration. Short-lived feature, fix, and documentation branches return through pull requests. Required Maven verification and review checks should protect shared branches. The project was not initialized as a Git repository here."),
("Chapter 10  Pull requests","ops","Focused commits make changes easier to review and revert. Pull requests should state behavior, tests, schema impacts, configuration changes, and secret handling. Branch protection must be configured on GitHub; Markdown guidance alone does not enforce merge checks."),
("Chapter 11  Jenkins pipeline","ops","The declarative pipeline checks out code, runs Maven clean verify, conditionally runs SonarQube, waits for a quality gate, then builds a Docker image. Surefire results and application artifacts are archived when available.","figure:pipe"),
("Chapter 11  CI setup","ops","Jenkins needs Java tool jdk21, Maven tool maven3, a SonarQube server named sonarqube, a sonar-token secret, and Docker access on the build agent. The names in the Jenkinsfile must match the installation configuration."),
("Chapter 12  SonarQube","ops","The project properties identify key, sources, tests, binaries, and JaCoCo XML. Jenkins uses credential binding for the token. No server, analysis, issue count, coverage, or gate result was available, so no quality score is reported."),
("Chapter 12  Quality interpretation","ops","Static analysis can find selected patterns but cannot prove that matches are correct or that privacy policy is satisfied. Coverage measures executed code paths, not correctness. Teams should set a quality profile before scanning and record the real result."),
("Chapter 13  Docker","ops","The Dockerfile builds with Maven and Java 21, then runs the packaged application in a smaller Java runtime image as a non-root user. Compose defines MySQL 8.4, a health check, named storage, and an app service that waits for database readiness."),
("Chapter 13  Environment configuration","ops","The sample environment file contains placeholder database, root, admin, and matching settings. Operators copy it to a private .env file and replace passwords. Compose connects to MySQL by service name. The application port is 8080 and MySQL port is 3306."),
("Chapter 13  Deployment and recovery","ops","The named database volume persists across normal restarts but is not a backup. A real deployment needs TLS, secret management, restricted database exposure, tested restores, logs, monitoring, resource limits, and a recovery procedure."),
("Chapter 14  Results","scope","The directory contains the Spring Boot application, templates, schema migration, matching service, security, notifications, audit events, tests, and DevOps configuration. These are source-level deliverables aligned with the campus proposal, not a verified release."),
("Chapter 14  Limitations","scope","Search loads open reports before filtering and has no pagination. There is no photo upload, external notification, recovery flow, rate limiting, user edit/withdraw route, or score calibration. Human verification is mandatory and false positives remain possible."),
("Chapter 15  Conclusion","scope","The project centralizes campus reports and ranks candidates through a deterministic score with visible factors. Its three-tier design, database schema, session security, notifications, staff review, tests, and CI/container configuration provide a coherent academic foundation."),
("Chapter 15  Future scope","scope","First compile and test the application, validate MySQL migrations, and inspect workflows in a browser. Then add pageable search, ownership-checked edit/withdraw, admin decision notes, stronger state transitions, identity integration, and notification delivery after privacy review."),
("Appendix A  Setup","ops","Install Java 21, Maven 3.9 or later, and optionally Docker. Copy .env.example to .env and set strong database and administrator passwords. Start MySQL, run Maven verification, then launch the application and open localhost on port 8080."),
("Appendix A  API reference","api","REST routes cover health, report search/create/read, current-user matches, and notification list/read. Requests use typed fields including date and optional time. Sessions and CSRF apply to POST requests. Pagination and generated OpenAPI are not yet included."),
("Appendix B  Data dictionary","data","The Flyway migration defines account identity and role, report details and status, candidate component scores, review status, notification read time, and admin audit fields. Foreign keys preserve ownership and pair relationships; unique constraints protect email and report pairs."),
("Appendix B  Matching example","matching","The total is category score times 0.25 plus description times 0.35, location times 0.25, and date/time times 0.15. Components range from 0 to 100. Identical values score highly; a date outside the window removes the date/time contribution."),
("Appendix C  References","scope","Official references include Spring Boot 3.5 documentation, Spring Security, Spring Data JPA, MySQL 8.4, Jakarta Bean Validation, Maven guides, JUnit 5, Jenkins handbook, SonarQube Server, and Docker Compose."),
("Appendix C  Traceability","scope","The slides specify project identity, problem, user groups, modules, architecture, development process, matching factors, and exclusions. Numeric weights come from Part 7 of the pasted request, not from a table visible in the slides. This report keeps those sources distinct."),
("Appendix D  File inventory","data","The source tree separates domain, repository, service, web, resources, tests, and documentation. Main operational files are pom.xml, application.yml, the Flyway migration, Jenkinsfile, Dockerfile, Compose, environment example, and Sonar properties."),
("Appendix D  Verification sign-off","tests","Record Java and Maven versions, command exit codes, test counts, migration result, registration, both report types, search, match explanation, notification ownership, admin review, quality gate, image status, and verified URL after execution.")
]
mods={
"scope":"The slide deck explicitly excludes AI/ML, GPS, facial recognition, payments, and distributed architecture. This prototype also names operational and product gaps rather than presenting them as implemented.",
"reports":"ReportController, ReportService, ItemReport, ReportRepository, and Flyway V1 implement the report data path. User edit and withdrawal are not available.",
"security":"AuthController, DatabaseUserDetailsService, SecurityConfig, and BootstrapConfig implement account loading and role rules. Public registration always assigns USER.",
"api":"ApiController and DTO records expose selected values. The browser and API share session security and state-changing browser requests require CSRF.",
"data":"Entities and Spring Data repositories define the persistence layer. MySQL is the intended runtime database; H2 is used only for test isolation.",
"matching":"MatchingService stores component scores and explanations. The model follows the pasted request's numeric table and is deterministic, not machine learning.",
"ui":"Thymeleaf templates and static CSS implement the screens. Escaped bindings protect displayed text; a live browser review has not been performed.",
"tests":"JUnit and MockMvc tests are included with an H2 test profile. Maven was not available, so these tests have not been run.",
"ops":"Maven, Jenkins, SonarQube, Docker, and Compose files configure a reproducible path. Tool installations, credentials, and services must be supplied."
}
implications={
"scope":"The scope decision favors an understandable campus prototype. Future additions should be justified by user evidence, institutional policy, and operational capacity rather than added only to increase technical complexity.",
"reports":"A report is useful only when users can describe the item and staff can interpret the same fields consistently. Category vocabulary and location names should be introduced with short examples and reviewed for local conventions.",
"security":"Authentication and authorization protect different boundaries. Signing in establishes an account; role checks restrict administrative actions; ownership-scoped queries prevent users from acting on another account's private notifications.",
"api":"Request and response records form the boundary between HTTP and persistence. Keeping those types explicit makes validation and field exposure reviewable, even as entity relationships evolve.",
"data":"Relational constraints protect invariants even when application code has a race or a defect. They should be paired with transaction handling and migration review, not treated as a replacement for either.",
"matching":"Component values let reviewers understand how a total was produced. Changing a weight changes rankings, so any configuration change should be recorded and validated against a stable set of example pairs.",
"ui":"A polished screen still needs evidence from real viewport and keyboard inspection. Design assets should clarify the next action and avoid suggesting that a candidate score means the item is already claimed.",
"tests":"A test is useful when it expresses an observable contract. Keep fixtures synthetic, assert boundary conditions, and separate unit logic from database-specific migration checks.",
"ops":"Configuration files describe intended behavior but do not prove the service is installed or running. A deployment record should capture tool versions, command output, image identity, and the environment used.",
}
practice={
"scope":"A demonstration should stay within these boundaries. Avoid presenting excluded capabilities as if they exist, and use synthetic records so a walkthrough does not expose a real lost item's identifying details. A scoped prototype is easier to evaluate because its actual behavior and remaining work remain visible.",
"reports":"A report workflow should preserve a clear owner and status from entry to resolution. Keep user actions distinct from staff decisions, and check the lifecycle after every change. Future edit or withdrawal endpoints must verify ownership before accepting requests and should preserve an audit record when status changes.",
"security":"Treat every route as a separate access decision: public content, authenticated user functions, and administrator functions. Verify both permitted and denied paths. Avoid returning account information in search results, keep CSRF enabled for browser writes, and protect the bootstrap administrator secret through environment configuration.",
"api":"Review the API boundary for field exposure, status codes, and authentication. Validate requests before service work; responses should not serialize entities or internal relationships. Before external clients depend on these routes, add pagination, a generated API schema, and compatibility rules for future changes.",
"data":"Review database changes as migrations, not inferred entity definitions. Check foreign keys, indexes, nullability, and unique constraints against the target MySQL version. Keep test data isolated, and perform migration and restore exercises against disposable databases before using production data.",
"matching":"Retain the component scores that were actually used for each total. A reviewer should be able to reproduce the arithmetic from configured weights. Record configuration changes alongside releases, and compare candidate scores with staff decisions to detect drift or inappropriate thresholds.",
"ui":"The interface should communicate what the user can do next and what the system knows. Use empty states when no reports exist, and keep keyboard focus visible. Review the rendered pages at desktop and phone widths before calling the experience complete.",
"tests":"Run unit and integration tests separately when diagnosing failures. Unit tests isolate score behavior, while integration tests reveal binding, database, and security interactions. Preserve Surefire output, investigate skips, and rerun full verification after a fix so results describe one consistent source revision.",
"ops":"The delivery path needs local configuration beyond repository files. Jenkins tool names, SonarQube server, credentials, and Docker permissions must align with the pipeline. Keep secrets out of logs and source control, capture image tags, and document the environment before reporting deployment results."
}
limits=[
"The authoring environment did not provide usable Maven or Docker commands. No build, test, image, quality gate, or deployment result is claimed.",
"MySQL migration and browser rendering require execution on a configured Java 21 host before the application is considered operational.",
"The matching threshold and rules are uncalibrated against institutional history; staff verification remains necessary.",
"The container stack targets local demonstration. Production requires managed secrets, TLS, backups, monitoring, and access review."
]
def field(p,code,placeholder):
    r=p.add_run();b=OxmlElement("w:fldChar");b.set(qn("w:fldCharType"),"begin");i=OxmlElement("w:instrText");i.set(qn("xml:space"),"preserve");i.text=code;s=OxmlElement("w:fldChar");s.set(qn("w:fldCharType"),"separate");t=OxmlElement("w:t");t.text=placeholder;e=OxmlElement("w:fldChar");e.set(qn("w:fldCharType"),"end")
    for z in (b,i,s,t,e):r._r.append(z)

doc=Document();sec=doc.sections[0];sec.top_margin=Inches(.68);sec.bottom_margin=Inches(.68);sec.left_margin=Inches(.78);sec.right_margin=Inches(.78)
n=doc.styles["Normal"];n.font.name="Aptos";n.font.size=Pt(10.5);n.font.color.rgb=RGBColor.from_string("243A45");n.paragraph_format.space_after=Pt(7);n.paragraph_format.line_spacing=1.1
for name,size,color in [("Title",32,NAVY),("Heading 1",20,NAVY),("Heading 2",15,TEAL),("Heading 3",12,NAVY)]:
    s=doc.styles[name];s.font.name="Aptos Display";s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=RGBColor.from_string(color.replace("#",""));s.paragraph_format.keep_with_next=True
header=sec.header.paragraphs[0];header.text="LOST-ITEM INTELLIGENCE NETWORK  |  PROJECT REPORT";header.style="Caption"
for r in header.runs:r.font.color.rgb=RGBColor.from_string(TEAL.replace("#",""))
f=sec.footer.paragraphs[0];f.alignment=WD_ALIGN_PARAGRAPH.RIGHT;f.add_run("Academic prototype  |  ");field(f," PAGE ","1")

p=doc.add_paragraph();p.paragraph_format.space_before=Pt(95);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("LOST-ITEM");r.bold=True;r.font.size=Pt(15);r.font.color.rgb=RGBColor.from_string(TEAL.replace("#",""))
p=doc.add_paragraph(style="Title");p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("Intelligence Network")
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("An Intelligent Lost-and-Found Management System");r.font.size=Pt(17);r.font.color.rgb=RGBColor.from_string(GREY.replace("#",""))
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(35);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("Software Engineering Project Report").bold=True
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("Java 21  |  Spring Boot 3.5  |  MySQL 8.4  |  Maven  |  JUnit 5")
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(70);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run("Prepared from the supplied Review 1 project materials\n28 October 2026")
p=doc.add_paragraph();p.paragraph_format.space_before=Pt(80);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("ACADEMIC PROTOTYPE");r.bold=True;r.font.size=Pt(10);r.font.color.rgb=RGBColor.from_string(TEAL.replace("#",""))
doc.add_page_break()
doc.add_heading("Executive Summary",level=1)
for text in [
"The Lost-Item Intelligence Network is a campus-oriented web application for centralized lost and found reports. Users can create a report, search open reports, and see possible connections. A deterministic matching service calculates component scores and stores pairs above a configurable threshold for administrative review.",
"The project uses Java 21, Spring Boot 3.5, Thymeleaf, Spring Security, Spring Data JPA, Hibernate, MySQL, Flyway, Maven, JUnit 5, Jenkins, SonarQube, and Docker Compose. Source artifacts include account registration, role-based administration, reporting, search, explanations, notices, audit events, responsive templates, a migration, tests, and build/deployment configuration.",
"The numeric weights come from Part 7 of the pasted request: category 25%, description 35%, location 25%, date/time 15%. The slide deck names the factors but does not print these numbers. The default threshold is 55% and is configurable. Similarity is a lead for review, not proof of ownership.",
"Maven and Docker were not available as usable commands in the authoring environment. No compilation, test, database, browser, quality gate, image build, or live deployment result is claimed."
]:doc.add_paragraph(text)
doc.add_page_break()
doc.add_heading("Report Guide and Abbreviations",level=1)
doc.add_paragraph("Chapters 1–3 describe the problem and requirements. Chapters 4–6 explain architecture, data, security, and workflows. Chapters 7–8 cover matching and interface design. Chapters 9–13 document tests and DevOps. Chapters 14–15 discuss results and future work. Appendices provide setup, API, schema, and references.")
doc.add_paragraph("Diagrams are conceptual illustrations generated from source structure, not screenshots or runtime traces. This report separates supplied requirements, source-level implementation, and execution results that remain pending.")
t=doc.add_table(rows=1,cols=2);t.style="Light Shading Accent 1";t.alignment=WD_TABLE_ALIGNMENT.CENTER;t.rows[0].cells[0].text="Term";t.rows[0].cells[1].text="Meaning"
for a,b in [("API","Application Programming Interface"),("CI","Continuous Integration"),("CSRF","Cross-Site Request Forgery"),("DTO","Data Transfer Object"),("JPA","Jakarta Persistence API"),("ORM","Object-Relational Mapping"),("RBAC","Role-Based Access Control"),("REST","Representational State Transfer")]:
    c=t.add_row().cells;c[0].text=a;c[1].text=b
doc.add_page_break()
doc.add_heading("Contents",level=1);field(doc.add_paragraph(),' TOC \\o "1-2" \\h \\z \\u ',"Open in Word and update the table of contents field.")
doc.add_paragraph("Chapter headings use Word heading styles, allowing the field to refresh after edits.")
doc.add_page_break()

seen_chapters=set()
for i,(title,kind,body,*extra) in enumerate(pages):
    if title.startswith("Chapter "):
        number=title.split()[1];level=1 if number not in seen_chapters else 2;seen_chapters.add(number)
    else: level=1 if title.startswith("Appendix") else 2
    doc.add_heading(title,level=level);doc.add_paragraph(body)
    p=doc.add_paragraph();r=p.add_run("Implementation note. ");r.bold=True;p.add_run(mods[kind])
    p=doc.add_paragraph();r=p.add_run("Design implication. ");r.bold=True;p.add_run(implications[kind])
    p=doc.add_paragraph();r=p.add_run("Review practice. ");r.bold=True;p.add_run(practice[kind])
    p=doc.add_paragraph();r=p.add_run("Verification boundary. ");r.bold=True;p.add_run(limits[i%len(limits)])
    if extra and extra[0].startswith("figure:"):
        key=extra[0].split(":")[1];path={"arch":arch,"flow":flow,"db":db,"pipe":pipe}[key]
        doc.add_picture(str(path),width=Inches(6.55));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
        cap=doc.add_paragraph("Figure. Conceptual design illustration derived from project source.");cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
        for r in cap.runs:r.italic=True;r.font.size=Pt(8)
    if title=="Chapter 8  Screenshot evidence":
        doc.add_picture(str(placeholder_path),width=Inches(6.4));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    if extra and extra[0]=="weights":
        t=doc.add_table(rows=1,cols=2);t.style="Light Shading Accent 1";t.rows[0].cells[0].text="Factor";t.rows[0].cells[1].text="Weight"
        for a,b in [("Category similarity","25%"),("Description similarity","35%"),("Location similarity","25%"),("Date/time similarity","15%")]:
            c=t.add_row().cells;c[0].text=a;c[1].text=b
    doc.add_page_break()

doc.add_heading("Appendix E  Verification Sign-off",level=1)
for label in ["Java and Maven versions","Command and exit code","JUnit passed, failed, skipped","MySQL migration","Registration and login","Lost and found report flow","Search and match explanation","Notification ownership","Administrator review and audit","SonarQube quality gate","Docker image and Compose","Verified URL and timestamp"]:
    p=doc.add_paragraph();r=p.add_run(label+": ");r.bold=True;p.add_run("Complete after execution; no result is asserted here.")
doc.add_paragraph("Complete this sign-off on a host with Java 21, Maven, MySQL or Docker, and a browser. Preserve logs, test reports, migration output, and actual screenshots so another reviewer can reproduce the results.")
doc.core_properties.title="Lost-Item Intelligence Network Project Report";doc.core_properties.subject="Full-stack campus lost-and-found application";doc.core_properties.author="Lost-Item Intelligence Network Project Team"
u=OxmlElement("w:updateFields");u.set(qn("w:val"),"true");doc.settings.element.append(u);doc.save(OUT)
print(f"Created {OUT}; topic pages: {len(pages)}")
