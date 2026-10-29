from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

OUT = Path(r'C:\Users\cheel\Downloads\lost-item-intelligence-network\PROJECT_MODULES_REPORT.docx')
NAVY, TEAL, PALE, INK, MUTED, WHITE = '17364A', '168A85', 'F3F6F5', '243B4A', '637783', 'FFFFFF'
doc = Document()
sec = doc.sections[0]
sec.top_margin=Inches(.78); sec.bottom_margin=Inches(.72); sec.left_margin=Inches(.82); sec.right_margin=Inches(.82)
sec.header_distance=Inches(.34); sec.footer_distance=Inches(.34)
styles=doc.styles
normal=styles['Normal']; normal.font.name='Arial'; normal.font.size=Pt(10.5); normal.font.color.rgb=RGBColor.from_string(INK)
normal.paragraph_format.space_after=Pt(6); normal.paragraph_format.line_spacing=1.12
for name,size,color in [('Title',29,NAVY),('Subtitle',14,MUTED),('Heading 1',19,NAVY),('Heading 2',13,TEAL),('Heading 3',11,NAVY)]:
    st=styles[name]; st.font.name='Arial'; st.font.size=Pt(size); st.font.color.rgb=RGBColor.from_string(color); st.font.bold=name!='Subtitle'; st.paragraph_format.keep_with_next=True; st.paragraph_format.space_before=Pt(14 if name.startswith('Heading') else 0); st.paragraph_format.space_after=Pt(5 if name.startswith('Heading') else 7)
styles['List Bullet'].font.name='Arial'; styles['List Bullet'].font.size=Pt(10.5); styles['List Bullet'].paragraph_format.space_after=Pt(3)
hp=sec.header.paragraphs[0]; hp.text='LOST-ITEM INTELLIGENCE NETWORK  |  FULL MODULE REPORT'; hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
for r in hp.runs: r.font.name='Arial'; r.font.size=Pt(8); r.font.color.rgb=RGBColor.from_string(MUTED); r.font.bold=True
fp=sec.footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=fp.add_run('Project module report  ·  '); r.font.name='Arial'; r.font.size=Pt(8); r.font.color.rgb=RGBColor.from_string(MUTED)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); fp._p.append(fld)

def shade(cell,color):
    tcPr=cell._tc.get_or_add_tcPr(); el=OxmlElement('w:shd'); el.set(qn('w:fill'),color); tcPr.append(el)
def margins(cell):
    tcPr=cell._tc.get_or_add_tcPr(); mar=OxmlElement('w:tcMar')
    for side,val in [('top',80),('start',100),('bottom',80),('end',100)]:
        e=OxmlElement('w:'+side); e.set(qn('w:w'),str(val)); e.set(qn('w:type'),'dxa'); mar.append(e)
    tcPr.append(mar)
def no_split(row): row._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))
def table(headers,rows,widths=None,font=9.2):
    t=doc.add_table(rows=1,cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'; t.autofit=False
    for j,val in enumerate(headers):
        c=t.rows[0].cells[j]; c.text=str(val); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER; shade(c,NAVY); margins(c)
        if widths: c.width=Inches(widths[j])
        for p in c.paragraphs:
            p.paragraph_format.space_after=Pt(0)
            for run in p.runs: run.font.name='Arial'; run.font.size=Pt(font); run.font.bold=True; run.font.color.rgb=RGBColor.from_string(WHITE)
    trPr=t.rows[0]._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:tblHeader')); no_split(t.rows[0])
    for i,row in enumerate(rows):
        cells=t.add_row().cells; no_split(t.rows[-1])
        for j,val in enumerate(row):
            c=cells[j]; c.text=str(val); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.TOP; margins(c)
            if i%2: shade(c,PALE)
            if widths: c.width=Inches(widths[j])
            for p in c.paragraphs:
                p.paragraph_format.space_after=Pt(1); p.paragraph_format.line_spacing=1.0
                for run in p.runs: run.font.name='Arial'; run.font.size=Pt(font); run.font.color.rgb=RGBColor.from_string(INK)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)
    return t
def para(text='',style=None): return doc.add_paragraph(text,style=style)
def bullet(text): return para(text,'List Bullet')
def h(text,level=1): return para(text,f'Heading {level}')
def note(text):
    p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(7); r=p.add_run(text); r.italic=True; r.font.size=Pt(9); r.font.color.rgb=RGBColor.from_string(MUTED)

# Cover
p=doc.add_paragraph(style='Title'); p.paragraph_format.space_before=Pt(86); p.add_run('Lost-Item Intelligence Network\nFull Module Report')
p=doc.add_paragraph(style='Subtitle'); p.paragraph_format.space_after=Pt(25); p.add_run('Architecture, module responsibilities, interfaces, data, and current verification')
p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(12); r=p.add_run('Prepared 29 October 2026'); r.font.size=Pt(12); r.font.bold=True; r.font.color.rgb=RGBColor.from_string(TEAL)
para('Java 21  |  Spring Boot 3.5.16  |  Thymeleaf  |  Spring Security  |  MySQL 8.4  |  Docker')
para('Purpose: document every implemented application module for project review, demonstration, and maintenance.')
para('Status: the local application, database connection, sign-in, dashboards, administrator review, and automated tests have been verified. External GitHub, Jenkins, and SonarQube service connections are not yet live.')
doc.add_page_break()

h('Executive Summary')
para('The Lost-Item Intelligence Network is a campus-focused web application for posting lost and found item reports, searching open reports, and identifying plausible lost/found pairs. Students and staff use browser accounts to submit reports. A deterministic matching service compares category, description, location, and date/time, stores qualifying candidates with component explanations, and sends a notice to each report owner. An administrator reviews candidates and records a confirmation or rejection.')
para('The implementation is organized into Spring Boot web controllers, services, Spring Data repositories, JPA domain entities, Thymeleaf pages, and a MySQL schema managed by Flyway. Browser form submissions use Spring Security sessions and CSRF protection. REST endpoints share the same session-based security model. Administrator-only actions create audit records.')
para('The current local verification state is positive for core workflows: 18 Maven tests pass; the Docker-hosted application responds on port 8091; MySQL has applied Flyway migration v1; the health endpoint returned HTTP 200; and student and administrator dashboards loaded with seeded match data. The Jenkinsfile and SonarQube properties are present, but no configured GitHub remote, live Jenkins run, or SonarQube analysis is claimed.')
h('Current Verification Snapshot',2)
table(['Area','Current evidence'],[
('Automated tests','18 passed: 12 matching unit tests, 5 account/report integration tests, and 1 application-context test.'),
('Local application','Docker container reachable at http://localhost:8091; host port 8080 was already occupied by another Java process.'),
('Database','MySQL 8.4 connected; Flyway schema v1 applied; seeded reports and matches are present.'),
('Live browser checks','Student dashboard and administrator review page render match titles; health endpoint returned HTTP 200.'),
('Demo records','5 named demo students; 12 reports (6 LOST, 6 FOUND); 6 candidate pairs (1 CONFIRMED, 5 PENDING); 12 notices for demo accounts.'),
('CI services','Jenkinsfile and SonarQube properties are in the project; external GitHub/Jenkins/SonarQube execution is not verified.')], [1.55,5.8])
h('Report Contents')
for x in ['01 System architecture and request flow','02 Application startup and configuration','03 Accounts authentication and roles','04 Lost and found report management','05 Search and discovery','06 Matching engine','07 User dashboard and notifications','08 Administrator review and audit','09 REST API','10 Persistence and schema','11 Browser interface','12 Validation and error handling','13 Automated tests and live verification','14 Docker runtime and operations','15 GitHub Jenkins and SonarQube integration status','16 Demonstration data and walkthrough','17 Limitations and next steps','Appendix A Source file map','Appendix B Database table reference','Appendix C API route reference','Appendix D References']: bullet(x)

h('01 System Architecture and Request Flow')
para('The application follows a three-layer design. The presentation layer consists of browser pages rendered by Thymeleaf and a CSS stylesheet. The application layer consists of Spring MVC controllers, security filters, services, and validation. The data layer consists of Spring Data JPA repositories, Hibernate entities, MySQL, and a Flyway migration.')
table(['Layer','Responsibilities','Representative components'],[
('Presentation','Collect input; show reports, match explanations, notices, and review controls.','Thymeleaf templates, fragments.html, app.css'),
('Application','Authenticate; validate; apply report, search, matching, notification, and review rules.','SecurityConfig, AuthController, ReportController, AdminController, ReportService, MatchingService'),
('Data','Persist accounts and activity; enforce relations and uniqueness; evolve schema.','JPA entities, repositories, MySQL 8.4, V1 migration')], [1.05,3.15,3.15])
h('Request path',2)
for x in [
'A browser request passes through Spring Security. Public pages are permitted; report and dashboard functions require an authenticated session; administration routes require the ADMIN role.',
'A submitted form is protected by a CSRF token, binds to a typed form object, and is validated before the controller calls a service.',
'ReportService saves a report in a transaction and asks MatchingService to compare it with open reports of the opposite type.',
'When a pair meets the configured threshold, the service stores one PotentialMatch and two owner notifications. A unique database constraint and repository check prevent duplicate pairs.',
'Controllers pass results to Thymeleaf or map them to API DTO records. Match queries fetch both linked reports so the dashboard and review templates can render titles after the database transaction closes.'
]: bullet(x)

h('02 Application Startup and Configuration')
para('LostItemApplication is the Spring Boot entry point. application.yml reads server settings, database connection values, matching weights, threshold, and date window from environment variables, with defaults for match parameters. It optionally imports a local .env file. The .env file is listed in .gitignore.')
para('At startup, Spring Boot validates database mappings, Flyway applies pending migrations, Spring Data configures repositories, and BootstrapConfig creates the configured administrator only if that email is not already present. The health route returns a small UP response and is intentionally public.')
h('Configuration groups',2)
table(['Setting group','Examples','Purpose'],[
('Server','SERVER_PORT','Application listener port; container listens on 8080 internally.'),
('Database','DB_URL, DB_USERNAME, DB_PASSWORD','JDBC connection to MySQL; Compose routes the app to service db.'),
('Initial administrator','INITIAL_ADMIN_EMAIL, INITIAL_ADMIN_PASSWORD','Bootstrap an ADMIN once for a new database.'),
('Matching','MATCH_CATEGORY_WEIGHT, MATCH_DESCRIPTION_WEIGHT, MATCH_LOCATION_WEIGHT, MATCH_DATE_WEIGHT, MATCH_THRESHOLD, MATCH_DATE_WINDOW_DAYS','Tune component contributions, candidate cutoff, and date window.')], [1.4,3.25,2.7])
note('Changing the configured bootstrap password after the admin account already exists does not reset the stored BCrypt password; the bootstrap runner creates only missing accounts.')

h('03 Accounts Authentication and Roles')
para('AuthController serves sign-in and registration pages and handles account creation. Registration validates a nonblank name, syntactically valid email, and password length from 10 through 72 characters. The controller checks for duplicate email addresses case-insensitively, trims the submitted name and email, lowercases the email, hashes the password with BCrypt, and assigns the USER role.')
para('DatabaseUserDetailsService loads an account by email without case sensitivity and trims surrounding whitespace from the submitted login identifier. It builds Spring Security authorities from the stored role. SecurityConfig uses session-based form login and redirects successful sign-ins to the dashboard. The forms use Thymeleaf th:action so Spring Security supplies the CSRF field.')
h('Access policy',2)
table(['Route group','Access rule'],[
('Home, sign-in, registration, static CSS/JS, health','Public'),('Reports, search, dashboard, user API','Authenticated session'),('/admin/** and /api/admin/**','ADMIN role'),('POST browser forms','CSRF token required')], [3.3,4.05])
note('The prototype does not include email verification, password reset, account recovery, multi-factor authentication, account lockout, or campus single sign-on.')

h('04 Lost and Found Report Management')
para('ReportController provides the home page, report form, report detail, current-user dashboard, and browser report submission. ReportService implements creation, per-user report retrieval, and open-report search. ItemReport stores a LOST or FOUND record and links it to its owner account.')
h('Report inputs and checks',2)
table(['Field','Rule'],[
('type','Required enum value: LOST or FOUND.'),('title','Required; up to 80 characters.'),('category','Required; up to 40 characters.'),('description','Required; up to 2,000 characters.'),('location','Required; up to 120 characters.'),('itemDate','Required and not in the future.'),('itemTime','Optional local time.')], [1.55,5.8])
para('The service trims report text before persistence, assigns the authenticated account as owner, and invokes the matching service in the same transaction. New reports begin with OPEN status. Administrators can move reports through review, resolved, or rejected states.')

h('05 Search and Discovery')
para('The search page and GET /api/reports use ReportService.search. The service returns open reports, optionally narrows the set to LOST or FOUND, and filters a query against title, description, category, and location using a case-folded string search. Results are ordered newest first before the text filter is applied.')
para('This is a simple lexical search, not a full-text or geospatial index. It does not rank by relevance or calculate distance between locations. The location field supports descriptive campus labels such as a building and area.')

h('06 Matching Engine')
para('MatchingService evaluates a new OPEN report against open reports of the opposite type. Its default weights are Category 25%, Description 35%, Location 25%, and Date/Time 15%. The weighted sum is limited to 0–100. A score of 55% or higher is stored as a candidate by default; weights, threshold, and the 30-day date window are configurable.')
table(['Component','Weight','Scoring rule'],[
('Category','25%','Normalized exact category match is 100; known synonyms map to canonical categories; other mismatches score 0.'),
('Description','35%','Jaccard overlap of normalized, unique word tokens.'),
('Location','25%','Normalized exact match is 100; containment in either direction is 75; otherwise 0.'),
('Date/Time','15%','Date similarity decays linearly to zero over 30 days. If both times exist, combine 70% date and 30% time similarity.')], [1.2,1.0,5.15])
para('Text normalization folds case, removes diacritics, trims and collapses whitespace, then tokenizes descriptions. Repeated words do not increase the score. Category synonym groups include phone/mobile/cell phone/laptop/computer/tablet as electronics; wallet/purse/keychain as accessories; and backpack/rucksack/handbag as bags. Location comparison is lexical and does not use coordinates.')
para('When both reports include times, the service measures the shorter difference on a 24-hour clock and linearly reduces the time score across a 12-hour half-day. If either time is absent, the date-only score is used. Each stored candidate includes the four component scores and a plain-language explanation with shared terms and date/time detail.')
note('The model is deterministic, interpretable, and unit-tested. It is not machine learning. The 55% threshold is a demonstration default and has not been calibrated against reviewed institutional history.')

h('07 User Dashboard and Notifications')
para('The dashboard lists the signed-in user’s reports, matches involving those reports, and recent notifications. MatchRepository uses an entity graph to fetch both lost and found report records along with candidate matches. This prevents lazy initialization errors when Thymeleaf renders titles after the service transaction ends. The same fetch strategy supports the administrator review center.')
para('When a candidate pair is saved, MatchingService creates two Notification records, one for each owner. The wording says that a possible connection is ready for review; it does not assert ownership. The API returns the most recent 30 notifications for the current user and supports a user-scoped mark-as-read action.')

h('08 Administrator Review and Audit')
para('AdminController serves /admin and its state-changing actions. The review center displays candidate pairs and open reports. An administrator can confirm or reject a match and change an item report status. Unsupported match decisions are rejected. Each review or status change writes an AuditEvent with actor, action, target type, target identifier, and event time.')
para('Candidate review state is held on PotentialMatch. A confirmed candidate is a human decision, not an automatic ownership assertion. Report and match changes are transactional with the corresponding audit record.')

h('09 REST API')
para('ApiController exposes JSON representations through /api. It uses DTO records rather than returning complete persistence entities. Except for the health route, API routes use the application session security rules. Mutating requests remain protected by CSRF.')
table(['Method and path','Access','Behavior'],[
('GET /api/health','Public','Returns service name and UP status.'),
('GET /api/reports?q=&type=','Authenticated','Searches open reports; type is optional LOST or FOUND.'),
('POST /api/reports','Authenticated','Validates and creates a report for the signed-in account.'),
('GET /api/reports/{id}','Authenticated','Returns one report DTO.'),
('GET /api/matches/mine','Authenticated','Returns matches involving the current user’s reports.'),
('GET /api/notifications/mine','Authenticated','Returns the current user’s recent notifications.'),
('POST /api/notifications/{id}/read','Authenticated','Marks only the current user’s notification as read.')], [2.35,1.25,3.75])
para('Report DTOs include id, type, title, category, description, location, date, optional time, and status. Match DTOs include report identifiers, total score, component scores, explanation, and review status. Notification DTOs expose message and timestamps.')

h('10 Persistence and Schema')
para('The persistence module uses JPA entities and Spring Data repositories. Hibernate validates mappings at startup while Flyway controls DDL. The initial migration creates five main tables and foreign keys. Open-in-view is disabled, so repository queries explicitly fetch the relationships needed by page rendering; the dashboard fix follows this rule.')
table(['Table','Purpose','Key relationships or constraints'],[
('app_users','Accounts and role data.','Unique email; role USER or ADMIN; password_hash contains BCrypt output.'),
('item_reports','Lost and found reports.','Owner foreign key; type/status, category, and date indexes.'),
('potential_matches','Candidate pair scores and review state.','Lost and found report foreign keys; unique pair; review index.'),
('notifications','Per-user candidate notices and read timestamps.','User and optional match foreign keys; user/read index.'),
('audit_events','Administrator change history.','Actor foreign key; target and actor/time indexes.')], [1.45,2.2,3.7])
para('MySQL 8.4 is used by the local runtime. The Compose database service stores data in the mysql_data named volume. The app reaches MySQL through internal Compose service name db when run as a container.')

h('11 Browser Interface')
para('The presentation module contains shared navigation and flash-message fragments, public landing and search pages, authentication forms, report entry and detail pages, the user dashboard, and the administrator review page. Thymeleaf binds form values and validation messages. Shared CSS provides responsive layouts and the application visual theme.')
table(['Template','Purpose'],[
('index.html','Public home and recent open reports.'),('login.html and register.html','Sign-in and account creation.'),('report-form.html and report-detail.html','Create a report and view report details.'),('search.html','Browse and filter open reports.'),('dashboard.html','Personal reports, matches, and notices.'),('admin.html','Review candidates and update report status.'),('fragments.html and app.css','Shared navigation, notices, footer, and styling.')], [2.55,4.8])

h('12 Validation and Error Handling')
para('Bean Validation annotations constrain report and registration forms before persistence. Controllers return form errors to the browser, while GlobalErrorHandler maps selected validation failures to HTTP 400 with field details, missing resources and records to HTTP 404, and invalid argument states to HTTP 400. The handler avoids returning database entities or stack traces as API responses.')
para('The application advises users to provide identifying descriptions without publishing private details. Matching notices say only that a possible connection exists; they do not expose hidden ownership data or claim item ownership.')

h('13 Automated Tests and Live Verification')
para('The Maven test suite was run on 29 October 2026. All 18 tests passed: 12 MatchingService tests, 5 AccountAndReportIntegrationTest cases, and 1 application-context test. Tests use an H2 in-memory database configured in MySQL compatibility mode and do not modify the live MySQL data.')
h('Coverage of the suite',2)
for x in [
'Matching tests cover exact fields, category synonyms, partial locations, Jaccard description scoring, date and optional-time behavior, bounded totals, thresholds, duplicate-pair prevention, and owner notices.',
'Account/report integration tests cover CSRF token rendering, registration, sign-in, report creation, dashboard match rendering, route authorization, and invalid registration.',
'Live checks confirmed MySQL connectivity, Flyway v1, the public health response, a student dashboard, and the administrator review page with seeded match titles.'
]: bullet(x)
note('The 18-test result is evidence from the local Maven run. It is not a Jenkins build, SonarQube quality gate, or production deployment record.')

h('14 Docker Runtime and Operations')
para('Dockerfile defines a two-stage build: a Maven/Java 21 builder packages the Spring Boot application, then a Java 21 runtime image runs the jar as a non-root user. compose.yaml defines a MySQL 8.4 service with a health check and named volume, plus an app service that waits for database readiness and receives environment configuration.')
para('The current local demonstration uses a Docker application container on host port 8091 mapped to container port 8080. The MySQL service runs in the Compose network. Host port 8080 was already in use by another Java process. The verified container runs the packaged application jar. A complete Dockerfile image build and the Jenkins-produced image path have not been verified.')
h('Local run commands',2)
for x in [
'Copy .env.example to .env and set DB_PASSWORD, MYSQL_ROOT_PASSWORD, and INITIAL_ADMIN_PASSWORD before first startup.',
'Start the database with docker compose up -d db, or start both services with docker compose up --build when the host port is available.',
'For the current runtime, open http://localhost:8091. The configured Compose mapping defaults to http://localhost:8080 on an available host.',
'Keep .env out of Git and do not publish its password values.'
]: bullet(x)

h('15 GitHub Jenkins and SonarQube Integration Status')
para('The project includes a Jenkinsfile, SonarQube project properties, a Dockerfile, Compose configuration, Maven dependencies, and a documented Git branching workflow. These files define the intended delivery process. They do not prove that external service accounts, webhooks, credentials, a remote repository, or a quality gate are connected.')
table(['Stage','Repository configuration','Current state'],[
('GitHub checkout','Jenkins uses checkout scm; docs describe main/develop/feature branching.','The project folder has no configured Git remote; webhook is not verified.'),
('Jenkins verification','Pipeline runs mvn -B clean verify and archives JUnit results and artifacts.','Maven verification passes locally; a Jenkins job has not been run.'),
('SonarQube','RUN_SONAR enables analysis and Quality Gate; server id sonarqube and secret id sonar-token are expected.','No server credentials, analysis, issue count, coverage score, or gate result are available.'),
('Docker build','Pipeline builds lost-item-intelligence-network:${BUILD_NUMBER}.','Local container runtime is verified; Jenkins image build/publish is not.')], [1.35,3.35,2.65])
para('Before describing the external pipeline as live, create and push the Git repository, configure Jenkins SCM/webhook and tool names jdk21 and maven3, add SonarQube server sonarqube and secret credential sonar-token, run the pipeline with RUN_SONAR=true, and record its actual quality-gate and Docker results.')

h('16 Demonstration Data and Walkthrough')
para('Five demonstration students were registered through the application. They use the USER role. Their records are fictional; the VIT Vellore building names are based on publicly listed campus facilities. The specific objects, dates, and sub-area descriptors are demonstration values.')
table(['Demo login','Password','Role'],[(f'student{i}@vit.student.ac.in','Student@1234','USER') for i in range(1,6)], [3.2,2.2,1.95])
note('These are shared local demo credentials created at the user’s request. Do not reuse them for real accounts or production access.')
table(['Lost report','Found report','Location','Score','Review'],[
('Black leather wallet','Wallet found at the central library','Periyar EVR Central Library','86.78','PENDING'),
('White 65W USB-C charger','USB-C wall adapter near TT lobby','Technology Tower','82.31','PENDING'),
('Navy backpack with yellow zipper','Navy backpack found at SJT','Silver Jubilee Tower','93.45','CONFIRMED'),
('Green steel water bottle','Green bottle found near Gandhi Block','Gandhi Block','88.94','PENDING'),
('Black wireless earbuds case','Earbuds case found at Anna Auditorium','Anna Auditorium','89.91','PENDING'),
('Blue ID lanyard and badge holder','Blue lanyard found at GDN Block','G. D. Naidu Block','83.54','PENDING')], [1.65,1.85,1.55,.75,1.55], 8.3)
para('The current database contains 12 reports, evenly split between LOST and FOUND, six candidate pairs, and 12 notifications for demo accounts. One backpack pair is confirmed; the other five pairs remain pending. Administrators can open /admin. A student can sign in to view owned reports, candidate matches, and notices on /dashboard.')

h('17 Limitations and Next Steps')
for x in [
'Connect a GitHub remote and configure a Jenkins SCM webhook before describing the delivery pipeline as live.',
'Run Jenkins verification, optional SonarQube analysis, and the Quality Gate; record actual build and quality results.',
'Build and test the Dockerfile image and, if required, configure a registry and deployment target.',
'Add account recovery, password change, email verification, and institutional SSO only after requirements and ownership are defined.',
'Calibrate the matching threshold and weights against reviewed examples before using match scores operationally.',
'Add pagination and OpenAPI documentation if report volume or integration requirements grow.'
]: bullet(x)
para('The application is a working local prototype. Core web workflows and deterministic matching are implemented and tested; external CI/CD services and production readiness controls remain incomplete.')

h('Appendix A Source File Map')
table(['Area','Key files'],[
('Startup and security','LostItemApplication.java; config/SecurityConfig.java; config/BootstrapConfig.java; service/DatabaseUserDetailsService.java'),
('Accounts and pages','web/AuthController.java; templates/login.html; templates/register.html'),
('Reports and search','web/ReportController.java; service/ReportService.java; repository/ReportRepository.java'),
('Matching','service/MatchingService.java; domain/PotentialMatch.java; repository/MatchRepository.java'),
('Notifications and audit','domain/Notification.java; domain/AuditEvent.java; repository/NotificationRepository.java; repository/AuditEventRepository.java'),
('Administration and API','web/AdminController.java; web/ApiController.java; web/GlobalErrorHandler.java'),
('Persistence and UI','resources/db/migration/V1__initial_schema.sql; resources/application.yml; resources/templates; resources/static/css/app.css'),
('Build and operations','pom.xml; Dockerfile; compose.yaml; Jenkinsfile; sonar-project.properties; .env.example'),
('Tests and guides','src/test/java; docs/API.md; docs/MATCHING.md; docs/BRANCHING.md; docs/DEMO_DATA.md')], [1.8,5.55])

h('Appendix B Database Table Reference')
para('The V1 migration defines five tables. Primary keys are generated numeric identifiers. Foreign-key constraints keep reports attached to owners, candidate pairs attached to both reports, notices attached to users and optional matches, and audit events attached to actors.')
for name,fields in [
('app_users','id, name, email, password_hash, role, created_at'),
('item_reports','id, type, title, category, description, location, item_date, item_time, status, owner_id, created_at, updated_at'),
('potential_matches','id, lost_report_id, found_report_id, score, category_score, description_score, location_score, date_time_score, explanation, review_status, created_at'),
('notifications','id, user_id, match_id, message, created_at, read_at'),
('audit_events','id, actor_id, action, target_type, target_id, occurred_at')]:
    h(name,2); para(fields)

h('Appendix C Project References')
for x in [
'Project README.md, docs/API.md, docs/MATCHING.md, docs/DEMO_DATA.md, application.yml, Jenkinsfile, compose.yaml, Dockerfile, and V1__initial_schema.sql.',
'VIT Vellore infrastructure and academic blocks: https://vit.ac.in/about/infrastructure/',
'Periyar EVR Central Library: https://vit.ac.in/academics/library',
'VIT Vellore hostels: https://vit.ac.in/campuslife/hostels'
]: bullet(x)

props=doc.core_properties; props.title='Lost-Item Intelligence Network Full Module Report'; props.subject='Complete module reference and current verification record'; props.keywords='Lost and found, Java, Spring Boot, MySQL, matching, Jenkins, Docker'
OUT.parent.mkdir(parents=True,exist_ok=True); doc.save(OUT)
word_count=sum(len(p.text.split()) for p in doc.paragraphs)+sum(len(c.text.split()) for t in doc.tables for row in t.rows for c in row.cells)
print(f'Created {OUT}; paragraphs={len(doc.paragraphs)} tables={len(doc.tables)} words={word_count}')
