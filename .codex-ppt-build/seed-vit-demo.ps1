$ErrorActionPreference = 'Stop'
$base = 'http://localhost:8091'
$password = 'Student@1234'
$students = 1..5 | ForEach-Object { [PSCustomObject]@{ Index=$_; Email="student$_@vit.student.ac.in"; Name="VIT Student $_" } }
$sessions = @{}
function Get-CsrfToken([string]$Url, $WebSession) {
  $page = Invoke-WebRequest -Uri $Url -WebSession $WebSession -UseBasicParsing
  $match = [regex]::Match($page.Content, 'name="_csrf"[^>]*value="([^"]+)"')
  if (-not $match.Success) { throw "Missing CSRF token on $Url" }
  return $match.Groups[1].Value
}
foreach ($student in $students) {
  $session = [Microsoft.PowerShell.Commands.WebRequestSession]::new()
  $token = Get-CsrfToken "$base/register" $session
  $created = Invoke-WebRequest -Uri "$base/register" -Method Post -Body @{ name=$student.Name; email=$student.Email; password=$password; _csrf=$token } -WebSession $session -UseBasicParsing -MaximumRedirection 5
  if ($created.Content -notmatch 'Account created') { throw "Registration did not complete for $($student.Email). The page may report a duplicate email or validation error." }
  $token = Get-CsrfToken "$base/login" $session
  [void](Invoke-WebRequest -Uri "$base/login" -Method Post -Body @{ username=$student.Email; password=$password; _csrf=$token } -WebSession $session -UseBasicParsing -MaximumRedirection 5)
  $dashboard = Invoke-WebRequest -Uri "$base/dashboard" -WebSession $session -UseBasicParsing -MaximumRedirection 5
  if ($dashboard.Content -notmatch 'Your campus activity') { throw "Login verification failed for $($student.Email)." }
  $sessions[$student.Index] = $session
}
$items = @(
  @{ owner=1; type='LOST'; title='Black leather wallet'; category='Accessories'; description='Black leather wallet with brass snap and two card slots; tiny blue stitch at the edge.'; location='Periyar EVR Central Library - study area'; date='2026-10-27'; time='10:00' },
  @{ owner=2; type='FOUND'; title='Wallet found at the central library'; category='Accessories'; description='Black leather wallet with brass snap and two card slots.'; location='Periyar EVR Central Library - study area'; date='2026-10-27'; time='10:15' },
  @{ owner=2; type='LOST'; title='White 65W USB-C charger'; category='Electronics'; description='White 65W USB-C wall charger with small AR initials on the label.'; location='Technology Tower - lobby'; date='2026-10-26'; time='13:30' },
  @{ owner=3; type='FOUND'; title='USB-C wall adapter near TT lobby'; category='Electronics'; description='White 65W USB-C power adapter; AR initials are written on the label.'; location='Technology Tower - lobby'; date='2026-10-26'; time='14:00' },
  @{ owner=3; type='LOST'; title='Navy backpack with yellow zipper'; category='Bags'; description='Dark navy backpack with a yellow zipper pull and a spiral notebook inside.'; location='Silver Jubilee Tower - entrance'; date='2026-10-24'; time='15:00' },
  @{ owner=4; type='FOUND'; title='Navy backpack found at SJT'; category='Bags'; description='Navy backpack with yellow zipper pull and notebook inside.'; location='Silver Jubilee Tower - entrance'; date='2026-10-24'; time='15:30' },
  @{ owner=4; type='LOST'; title='Green steel water bottle'; category='Drinkware'; description='Matte green steel water bottle with a silver loop and a small dent near the base.'; location='Gandhi Block - main entrance'; date='2026-10-27'; time='12:00' },
  @{ owner=5; type='FOUND'; title='Green bottle found near Gandhi Block'; category='Drinkware'; description='Green steel water bottle with silver loop and a slight dent near its base.'; location='Gandhi Block - main entrance'; date='2026-10-27'; time='12:20' },
  @{ owner=5; type='LOST'; title='Black wireless earbuds case'; category='Electronics'; description='Black wireless earbud charging case with one silver sticker on the lid.'; location='Anna Auditorium - entrance'; date='2026-10-23'; time='18:00' },
  @{ owner=1; type='FOUND'; title='Earbuds case found at Anna Auditorium'; category='Electronics'; description='Black wireless earbuds charging case with a small silver sticker on the lid.'; location='Anna Auditorium - entrance'; date='2026-10-23'; time='18:15' },
  @{ owner=1; type='LOST'; title='Blue ID lanyard and badge holder'; category='Accessories'; description='Blue fabric ID lanyard with clear plastic badge sleeve and a small star charm.'; location='G. D. Naidu Block - entrance'; date='2026-10-25'; time='11:00' },
  @{ owner=2; type='FOUND'; title='Blue lanyard found at GDN Block'; category='Accessories'; description='Blue lanyard with clear badge holder and a little star charm.'; location='G. D. Naidu Block - entrance'; date='2026-10-25'; time='11:20' }
)
foreach ($item in $items) {
  $session = $sessions[$item.owner]
  $token = Get-CsrfToken "$base/reports/new?type=$($item.type)" $session
  $result = Invoke-WebRequest -Uri "$base/reports" -Method Post -Body @{ type=$item.type; title=$item.title; category=$item.category; description=$item.description; location=$item.location; itemDate=$item.date; itemTime=$item.time; _csrf=$token } -WebSession $session -UseBasicParsing -MaximumRedirection 5
  if ($result.Content -notmatch [regex]::Escape($item.title)) { throw "Report did not publish: $($item.title)" }
}
"Created and verified $($students.Count) student accounts and $($items.Count) reports through the application."
