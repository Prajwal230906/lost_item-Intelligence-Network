import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const workspaceDir = 'C:/Users/cheel/Downloads/lost-item-intelligence-network';
const SKILL_DIR = 'C:/Users/cheel/.codex/plugins/cache/openai-primary-runtime/presentations/26.1025.11240/skills/presentations';
const TMP_DIR = path.join(workspaceDir, '.codex-ppt-build');
const FINAL_PPTX = path.join(workspaceDir, 'final-review', 'Lost_Item_Intelligence_Network_Final_Review.pptx');
const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, 'container_tools/artifact_tool_utils.mjs')).href);
const font = resolvePresentationFont();
const W = 1280, H = 720;
const C = {
  navy: '#102B3B', navy2: '#193D4E', teal: '#168A85', mint: '#69D9C7',
  paper: '#F6F7F3', white: '#FFFFFF', ink: '#183342', muted: '#647985',
  line: '#D5DFDA', paleTeal: '#E4F3EF', paleAmber: '#FFF2DC', amber: '#9A6715',
  green: '#18745F', paleGreen: '#E5F3EB', red: '#B4533C', paleBlue: '#EAF0F4',
};
const p = Presentation.create({ slideSize: { width: W, height: H } });
let shapeCounter = 0;
function tx(slide, value, x, y, w, h, opt = {}) {
  const sh = slide.shapes.add({
    geometry: 'textbox', name: opt.name || `text-${++shapeCounter}`,
    position: { left: x, top: y, width: w, height: h }, fill: 'none',
    line: { style: 'solid', fill: 'none', width: 0 },
  });
  sh.text = value;
  sh.text.style = {
    fontSize: opt.size ?? 24, typeface: font, color: opt.color ?? C.ink,
    bold: opt.bold ?? false, alignment: opt.align ?? 'left',
    verticalAlignment: opt.valign ?? 'top', wrap: 'square', autoFit: 'shrinkText', insets: 0,
  };
  return sh;
}
function box(slide, x, y, w, h, fill = C.white, stroke = C.line, strokeWidth = 1, name = `box-${++shapeCounter}`) {
  return slide.shapes.add({ geometry: 'rect', name, position: { left: x, top: y, width: w, height: h }, fill, line: { style: 'solid', fill: stroke, width: strokeWidth } });
}
function bar(slide, x, y, w, h, color) {
  return slide.shapes.add({ geometry: 'rect', name: `rule-${++shapeCounter}`, position: { left: x, top: y, width: w, height: h }, fill: color, line: { style: 'solid', fill: 'none', width: 0 } });
}
function circle(slide, x, y, d, fill, stroke = fill) {
  return slide.shapes.add({ geometry: 'ellipse', name: `dot-${++shapeCounter}`, position: { left: x, top: y, width: d, height: d }, fill, line: { style: 'solid', fill: stroke, width: 1 } });
}
function baseSlide(title, n, dark = false) {
  const s = p.slides.add();
  s.background.fill = dark ? C.navy : C.paper;
  const fg = dark ? C.white : C.ink;
  tx(s, title, 72, 43, 1136, 66, { size: 46, bold: true, color: fg, name: `slide-${n}-title` });
  bar(s, 72, 125, 1136, 2, dark ? '#315365' : C.line);
  if (!dark) {
    tx(s, 'LOST-ITEM INTELLIGENCE NETWORK', 72, 684, 700, 20, { size: 15, color: C.muted, bold: true });
    tx(s, String(n).padStart(2, '0'), 1166, 681, 42, 24, { size: 16, color: C.muted, bold: true, align: 'right' });
  }
  return s;
}
function bullet(slide, x, y, text, w = 500, opt = {}) {
  circle(slide, x, y + 10, 9, opt.dot ?? C.teal);
  tx(slide, text, x + 24, y, w - 24, opt.h ?? 56, { size: opt.size ?? 23, color: opt.color ?? C.ink, bold: opt.bold ?? false });
}
function arrow(slide, x, y, w = 55, color = C.teal) {
  bar(slide, x, y + 16, w - 13, 3, color);
  tx(slide, '›', x + w - 22, y - 3, 24, 44, { size: 44, color, bold: true, align: 'center', valign: 'middle' });
}

// 1 — Cover
{
  const s = p.slides.add(); s.background.fill = C.navy;
  bar(s, 78, 100, 58, 5, C.mint);
  tx(s, 'FINAL PROJECT REVIEW', 78, 128, 650, 32, { size: 19, color: C.mint, bold: true });
  tx(s, 'Lost-Item\nIntelligence Network', 78, 194, 820, 178, { size: 67, color: C.white, bold: true });
  tx(s, 'A campus lost-and-found web application with explainable matching and administrator review', 82, 408, 775, 86, { size: 27, color: '#D3E3E5' });
  bar(s, 82, 548, 1100, 1, '#315365');
  tx(s, 'JAVA 21  ·  SPRING BOOT  ·  MYSQL  ·  DOCKER', 82, 576, 900, 30, { size: 18, color: '#BCD2D7', bold: true });
  tx(s, 'Review build · 28 October 2026', 82, 634, 570, 25, { size: 17, color: '#9CB7BE' });
  tx(s, 'FINAL REVIEW', 1000, 634, 200, 25, { size: 16, color: C.mint, bold: true, align: 'right' });
}
// 2 — Problem and response
{
  const s = baseSlide('Problem and project goal', 2);
  tx(s, 'THE PROBLEM', 82, 165, 430, 30, { size: 18, color: C.teal, bold: true });
  tx(s, 'Reports are scattered.\nSearching by hand misses connections.', 82, 207, 490, 108, { size: 34, bold: true });
  bullet(s, 84, 342, 'Messages, notice boards, and counters split the information.', 472, { h: 56 });
  bullet(s, 84, 414, 'Descriptions are difficult to compare consistently.', 472, { h: 56 });
  bullet(s, 84, 486, 'Date and place details often go unused.', 472, { h: 56 });
  bar(s, 632, 174, 2, 420, C.line);
  tx(s, 'THE RESPONSE', 690, 165, 430, 30, { size: 18, color: C.teal, bold: true });
  tx(s, 'One campus service\nfor reports and review.', 690, 207, 500, 108, { size: 34, bold: true });
  bullet(s, 692, 342, 'Create a structured lost or found report.', 480, { h: 56 });
  bullet(s, 692, 414, 'Compare category, description, place, and date/time.', 480, { h: 56 });
  bullet(s, 692, 486, 'Show possible matches for a person to verify.', 480, { h: 56 });
  tx(s, 'The score helps find candidates; it does not prove ownership.', 82, 605, 1100, 32, { size: 19, color: C.muted, italic: true });
}
// 3 — Product capabilities
{
  const s = baseSlide('Application capabilities', 3);
  const left = [
    ['01  ACCOUNTS', 'Register and sign in with role-based access.'],
    ['02  REPORTS', 'Create lost and found reports with structured details.'],
    ['03  SEARCH', 'Browse and filter open reports.'],
  ];
  const right = [
    ['04  MATCHING', 'Calculate and explain candidate similarities.'],
    ['05  NOTICES', 'Notify report owners when a candidate pair appears.'],
    ['06  ADMIN REVIEW', 'Confirm or reject candidate matches and update status.'],
  ];
  for (let i=0;i<3;i++) {
    const y=178+i*142;
    tx(s,left[i][0],82,y,475,30,{size:18,color:C.teal,bold:true});
    tx(s,left[i][1],82,y+39,490,62,{size:24});
    tx(s,right[i][0],666,y,490,30,{size:18,color:C.teal,bold:true});
    tx(s,right[i][1],666,y+39,500,62,{size:24});
  }
  bar(s, 620, 170, 2, 440, C.line);
  tx(s, 'Prototype scope is campus-focused. GPS tracking, machine learning, and face recognition are out of scope.', 82, 622, 1110, 36, { size: 18, color: C.muted });
}
// 4 — Architecture
{
  const s = baseSlide('Application architecture', 4);
  const y=215, h=170;
  box(s,82,y,292,h,C.white,C.line,1,'browser-layer');
  tx(s,'PRESENTATION',104,y+22,250,27,{size:17,color:C.teal,bold:true});
  tx(s,'Browser + Thymeleaf',104,y+60,250,38,{size:26,bold:true});
  tx(s,'Login · Reports · Search\nDashboard · Admin review',104,y+108,250,50,{size:19,color:C.muted});
  arrow(s,390,278,65);
  box(s,470,y,342,h,C.white,C.line,1,'service-layer');
  tx(s,'APPLICATION',494,y+22,300,27,{size:17,color:C.teal,bold:true});
  tx(s,'Spring Boot services',494,y+60,300,38,{size:26,bold:true});
  tx(s,'Security · Validation\nMatching · Notifications · REST API',494,y+108,300,50,{size:19,color:C.muted});
  arrow(s,828,278,65);
  box(s,908,y,292,h,C.white,C.line,1,'data-layer');
  tx(s,'DATA',932,y+22,245,27,{size:17,color:C.teal,bold:true});
  tx(s,'MySQL + Flyway',932,y+60,250,38,{size:26,bold:true});
  tx(s,'Accounts · Reports\nMatches · Notices · Audit events',932,y+108,250,50,{size:19,color:C.muted});
  bar(s,82,454,1118,2,C.line);
  tx(s,'Spring Data JPA repositories connect application services to persistent records. Flyway creates and validates the schema at startup.',82,485,1080,70,{size:22,color:C.ink});
}
// 5 — User flow
{
  const s = baseSlide('Report-to-review workflow', 5);
  const steps = [
    ['Report item','A user posts a lost or found item.'],
    ['Save details','The app validates and stores the report.'],
    ['Compare','The service scores opposite-type reports.'],
    ['Show candidate','A score and field explanation are saved.'],
    ['Review','An administrator confirms or rejects.'],
    ['Notify','Owners see a possible connection.'],
  ];
  const x0=92, bw=318, gap=84, rowYs=[190,388];
  for(let i=0;i<steps.length;i++){
    const row=Math.floor(i/3), col=i%3, x=x0+col*(bw+gap), y=rowYs[row];
    circle(s,x,y,36,i===4?C.navy:C.teal);
    tx(s,String(i+1),x,y+4,36,28,{size:19,color:C.white,bold:true,align:'center',valign:'middle'});
    tx(s,steps[i][0],x,y+52,bw,36,{size:25,bold:true});
    tx(s,steps[i][1],x,y+94,bw,60,{size:21,color:C.muted});
    if(col<2) arrow(s,x+bw+16,y+87,gap-28,C.teal);
  }
  bar(s,82,570,1116,2,C.line);
  tx(s,'Example: a lost black wallet and a found wallet report share category, description, library location, and date.',82,590,1080,39,{size:19});
  tx(s,'An administrator makes the final decision; a similarity score is not proof of ownership.',82,633,1080,30,{size:17,color:C.muted,italic:true});
}
// 6 — Matching model
{
  const s = baseSlide('Explainable match score', 6);
  tx(s,'WEIGHTED SIGNALS',82,160,460,30,{size:18,color:C.teal,bold:true});
  const rows=[['Category',25],['Description',35],['Location',25],['Date / time',15]];
  for(let i=0;i<rows.length;i++){
    const y=208+i*82;
    tx(s,rows[i][0],82,y,220,31,{size:23,bold:true});
    box(s,330,y+4,465,24,'#E2E9E5','#E2E9E5',0,`score-track-${i}`);
    box(s,330,y+4,465*rows[i][1]/35,24,i===1?C.teal:'#66BDB0',i===1?C.teal:'#66BDB0',0,`score-bar-${i}`);
    tx(s,`${rows[i][1]}%`,825,y-1,82,34,{size:23,bold:true,color:C.ink,align:'right'});
  }
  bar(s,950,178,2,390,C.line);
  tx(s,'CANDIDATE RULE',986,182,230,26,{size:17,color:C.teal,bold:true});
  tx(s,'55%+',986,226,220,72,{size:56,bold:true,color:C.navy});
  tx(s,'is the configurable default threshold.',986,302,218,55,{size:20,color:C.muted});
  tx(s,'Date similarity declines over a 30-day window. If both times are supplied, time similarity contributes to the date/time component.',986,389,220,123,{size:19});
  tx(s,'Deterministic and explainable—not machine learning. Calibrate before operational use.',82,583,1115,49,{size:19,color:C.muted,italic:true});
}
// 7 — Security and data
{
  const s = baseSlide('Security and data handling', 7);
  const items=[
    ['PASSWORDS','BCrypt hashes are stored; raw passwords are not.'],
    ['ACCESS','Spring Security protects signed-in pages; admin routes require the ADMIN role.'],
    ['FORMS','CSRF tokens protect sign-in, account creation, and state-changing forms.'],
    ['PERSISTENCE','MySQL stores accounts and reports; Flyway controls schema changes.'],
  ];
  for(let i=0;i<items.length;i++){
    const col=i%2, row=Math.floor(i/2), x=82+col*588, y=190+row*198;
    tx(s,items[i][0],x,y,500,28,{size:18,color:C.teal,bold:true});
    tx(s,items[i][1],x,y+45,510,89,{size:25,bold:false});
    if(col===0) bar(s,640,y,2,142,C.line);
  }
  bar(s,82,588,1116,2,C.line);
  tx(s,'Prototype limitation: password change and account recovery are not included.',82,612,1110,34,{size:19,color:C.muted});
}
// 8 — Stack and run
{
  const s = baseSlide('Technology stack and local runtime', 8);
  const rows=[
    ['WEB','Java 21 · Spring Boot 3.5.16 · Thymeleaf'],
    ['DATA','Spring Data JPA · MySQL 8.4 · Flyway'],
    ['BUILD','Maven · JUnit 5 · Spring MockMvc'],
    ['CONTAINER','Docker · Compose · multi-stage Dockerfile'],
  ];
  for(let i=0;i<rows.length;i++){
    const y=171+i*88;
    tx(s,rows[i][0],82,y,195,29,{size:18,color:C.teal,bold:true});
    tx(s,rows[i][1],280,y-3,790,44,{size:26,bold:true});
    bar(s,82,y+58,1110,1,C.line);
  }
  tx(s,'Current verified local app',82,554,360,27,{size:17,color:C.teal,bold:true});
  tx(s,'http://localhost:8091',82,589,490,44,{size:30,bold:true,color:C.navy});
  tx(s,'Port 8091 is used because another Java process already occupies 8080.',590,590,590,52,{size:18,color:C.muted});
}
// 9 — Verification
{
  const s = baseSlide('Verification results', 9);
  tx(s,'17 / 17',82,177,405,92,{size:68,bold:true,color:C.teal});
  tx(s,'automated tests passed',84,270,450,41,{size:27,bold:true});
  tx(s,'12 matching unit tests\n4 account/report integration tests\n1 application context test',84,331,440,126,{size:22,color:C.muted});
  bar(s,572,179,2,375,C.line);
  tx(s,'LIVE LOCAL CHECKS',624,180,500,28,{size:18,color:C.teal,bold:true});
  bullet(s,626,230,'App connected to MySQL; Flyway v1 schema migration completed.',550,{h:55,size:21});
  bullet(s,626,307,'Configured admin sign-in reached the dashboard.',550,{h:55,size:21});
  bullet(s,626,384,'Public health endpoint returned HTTP 200.',550,{h:55,size:21});
  tx(s,'Verified in the local container on 28 October 2026. These checks do not represent a Jenkins or SonarQube run.',82,594,1110,54,{size:18,color:C.muted,italic:true});
}
// 10 — CI/CD architecture
{
  const s = baseSlide('CI/CD integration path', 10);
  tx(s,'PIPELINE DEFINED IN JENKINSFILE',82,153,800,28,{size:18,color:C.teal,bold:true});
  const nodes=[
    ['GitHub','SCM checkout','Remote not configured',C.paleAmber,C.amber],
    ['Jenkins','Pipeline stages','Not executed',C.paleAmber,C.amber],
    ['Maven + JUnit','clean verify','17 local tests pass',C.paleGreen,C.green],
    ['SonarQube','Optional quality gate','Needs server + token',C.paleAmber,C.amber],
    ['Docker','Build image','Container runtime verified',C.paleGreen,C.green],
  ];
  const x0=66,bw=194,gap=54,y=235,bh=203;
  for(let i=0;i<nodes.length;i++){
    const x=x0+i*(bw+gap);
    box(s,x,y,bw,bh,C.white,C.line,1,`pipeline-${i}`);
    tx(s,String(i+1).padStart(2,'0'),x+15,y+15,45,23,{size:16,color:C.teal,bold:true});
    tx(s,nodes[i][0],x+15,y+53,bw-30,55,{size:23,bold:true});
    tx(s,nodes[i][1],x+15,y+112,bw-30,37,{size:17,color:C.muted});
    bar(s,x+15,y+155,bw-30,1,C.line);
    tx(s,nodes[i][2],x+15,y+166,bw-30,30,{size:15,color:nodes[i][4],bold:true});
    if(i<nodes.length-1) arrow(s,x+bw+7,y+90,gap-8,C.teal);
  }
  tx(s,'Jenkins stages: checkout scm → mvn clean verify → optional SonarQube analysis + quality gate → docker build.',82,477,1110,64,{size:22,bold:true});
  tx(s,'The code defines the handoffs. GitHub remote/webhook, Jenkins credentials and a live SonarQube server still need to be configured and run.',82,560,1110,72,{size:19,color:C.muted});
  s.speakerNotes.text = 'The repository contains a Jenkinsfile with SCM checkout, Maven verification, an optional RUN_SONAR stage that uses Jenkins SonarQube and secret credential IDs, a Quality Gate wait, and a Docker build. The project folder currently has no Git repository remote, and no Jenkins or SonarQube run has been verified. Present this as the intended pipeline definition, not as an active external integration.';
}
// 11 — Review outcome
{
  const s = baseSlide('Final review status', 11);
  tx(s,'READY TO DEMONSTRATE',82,166,500,28,{size:18,color:C.green,bold:true});
  tx(s,'The app is running locally and the core flows are covered.',82,208,500,82,{size:31,bold:true});
  bullet(s,84,314,'Login, dashboard, report, and admin review are implemented.',490,{h:58,size:21,dot:C.green});
  bullet(s,84,392,'MySQL schema migration and admin sign-in verified live.',490,{h:58,size:21,dot:C.green});
  bullet(s,84,470,'17 automated tests pass.',490,{h:46,size:21,dot:C.green});
  bar(s,630,172,2,411,C.line);
  tx(s,'TO COMPLETE THE EXTERNAL PIPELINE',678,166,520,28,{size:18,color:C.amber,bold:true});
  tx(s,'Connect source control and CI services.',678,208,500,82,{size:31,bold:true});
  bullet(s,680,314,'Create/push the GitHub repository and add the Jenkins SCM webhook.',510,{h:58,size:21,dot:C.amber});
  bullet(s,680,392,'Configure Jenkins JDK/Maven tools and SonarQube credentials.',510,{h:58,size:21,dot:C.amber});
  bullet(s,680,470,'Run the Jenkins pipeline with RUN_SONAR=true and publish the image if required.',510,{h:68,size:21,dot:C.amber});
  tx(s,'Status distinction: local app and tests are verified; external GitHub, Jenkins, and SonarQube connections are not yet confirmed.',82,602,1110,46,{size:18,color:C.muted,italic:true});
}
// 12–14 — Screenshot spaces, deliberately left open for the user
const screenshotSlides = [
  ['Project screenshot 1 · Sign in and registration','Paste the sign-in or account-creation screen here.'],
  ['Project screenshot 2 · Reports and dashboard','Paste the user report list, search, or dashboard here.'],
  ['Project screenshot 3 · Admin match review','Paste the admin candidate-match review screen here.'],
];
for(let i=0;i<screenshotSlides.length;i++){
  const n=12+i; const s=baseSlide(screenshotSlides[i][0],n);
  box(s,92,166,1096,478,'#FBFCF9','#8FAEAC',2,`screenshot-frame-${n}`);
  tx(s,'PASTE PROJECT SCREENSHOT HERE',170,340,940,44,{size:27,color:'#6D8A8A',bold:true,align:'center',valign:'middle'});
  tx(s,screenshotSlides[i][1],180,394,920,38,{size:19,color:C.muted,align:'center'});
}

await fs.mkdir(TMP_DIR,{recursive:true});
await fs.mkdir(path.dirname(FINAL_PPTX),{recursive:true});
const draft = path.join(TMP_DIR,'final-review-draft.pptx');
const deckBlob = await PresentationFile.exportPptx(p);
await deckBlob.save(draft);
for (let i=0;i<p.slides.items.length;i++) {
  const png=await p.export({slide:p.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(TMP_DIR,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await png.arrayBuffer()));
}
const montage=await p.export({format:'webp',montage:true,scale:0.45});
await fs.writeFile(path.join(TMP_DIR,'montage.webp'),new Uint8Array(await montage.arrayBuffer()));
const requirements={explicitTotalSlideCount:14,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[]};
const result=await finalizePresentation({
  ...requirements, workspaceDir, candidatePath:draft, finalPath:FINAL_PPTX,
  pythonExecutable:'C:/Users/cheel/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe',
  integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
  fontPolicy:{basis:'design',families:[font]},
  verifyArtifactToolImport:true,
  receiptPath:path.join(TMP_DIR,'validation-final.json'),
});
console.log(JSON.stringify({font,slideCount:p.slides.items.length,draft,final:FINAL_PPTX,finalizer:result},null,2));



