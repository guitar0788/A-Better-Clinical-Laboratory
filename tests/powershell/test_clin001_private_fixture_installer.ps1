# Purely synthetic Windows PowerShell test; no game binaries, original XML,
# secrets, Steam install, persistent saves, or installed add-ons are accessed.
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$tmpRoot = Join-Path $env:RUNNER_TEMP ('clin001-test-' + [Guid]::NewGuid().ToString('N'))
$caseId = 'DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE'
$leadId = 'TRM_LDP'
$sampleId = 'EXM_ABCL_G1_BLOOD_LEAD_SAMPLING'

function Assert([bool] $condition,[string] $reason) {
  if (-not $condition) { throw "C1 fixture smoke FAIL: $reason" }
}

function Write-Xml([string] $path,[string] $data) {
  [IO.File]::WriteAllText($path,$data,[System.Text.UTF8Encoding]::new($false))
}

function New-TestGame([string]$label) {
  $root = Join-Path $tmpRoot ("Project Hospital " + $label)
  $assets = Join-Path $root 'ProjectHospital_Data\StreamingAssets'
  $db = Join-Path $assets 'Database'
  $diagnoses = Join-Path $db 'Diagnoses'
  $addons = Join-Path $assets 'Addons'
  New-Item -ItemType Directory -Path $diagnoses -Force | Out-Null
  New-Item -ItemType Directory -Path $addons -Force | Out-Null
  Write-Xml (Join-Path $db 'Departments.xml') @'
<Database><GameDBDepartment ID="DPT_LAB"><RequiredRoomsClinic>
<GameDBDepartmentRoomRequirement><RoomDatabaseEntryRef>ROOM_TYPE_HEMATOLOGY_LAB</RoomDatabaseEntryRef><MinCount>1</MinCount><MaxCount>2</MaxCount></GameDBDepartmentRoomRequirement>
</RequiredRoomsClinic></GameDBDepartment></Database>
'@
  Write-Xml (Join-Path $diagnoses 'DiagnosesER.xml') @'
<Database><GameDBMedicalCondition ID="DIA_CLD">
<DepartmentRef>DPT_EMERGENCY</DepartmentRef><Symptoms><GameDBSymptomRules><ProbabilityPercent>100</ProbabilityPercent><GameDBSymptomRef>SYM_SORE_THROAT</GameDBSymptomRef></GameDBSymptomRules></Symptoms>
<Examinations><ExaminationRef>EXM_INTERVIEW</ExaminationRef></Examinations><Treatments><TreatmentRef>TRT_REST</TreatmentRef></Treatments></GameDBMedicalCondition></Database>
'@
  Write-Xml (Join-Path $diagnoses 'DiagnosesINTERN.xml') @'
<Database><GameDBMedicalCondition ID="TRM_LDP">
<DepartmentRef>DPT_INTERNAL_MEDICINE_DEPARTMENT</DepartmentRef><Symptoms><GameDBSymptomRules><ProbabilityPercent>100</ProbabilityPercent><GameDBSymptomRef>SYM_LEAD_LEVELS_HIGH</GameDBSymptomRef></GameDBSymptomRules></Symptoms>
<Examinations><ExaminationRef>EXM_INTERVIEW</ExaminationRef></Examinations><Treatments><TreatmentRef>TRT_HOSPITALIZATION_HIGH_PRIORITY</TreatmentRef><TreatmentRef>TRT_CHELATION_THERAPY</TreatmentRef></Treatments></GameDBMedicalCondition></Database>
'@
  return @{root=$root; db=$db; addons=$addons}
}

function Test-Mode([bool]$nativeLead) {
  $label = if ($nativeLead) { 'R3' } else { 'R2' }
  $game = New-TestGame $label
  $fixtureInstaller = Join-Path $tmpRoot ("installer-" + $label)
  New-Item -ItemType Directory -Path $fixtureInstaller | Out-Null
  Copy-Item -LiteralPath (Join-Path $repoRoot 'tools\Install-ABCL-G1.ps1') -Destination $fixtureInstaller
  $addonSource = Join-Path $fixtureInstaller 'ModABCLG1LeadTest'
  New-Item -ItemType Directory -Path (Join-Path $addonSource 'Database') -Force | Out-Null
  # The installer tests only DLL existence; this is a deliberately fake
  # source-file sentinel and MUST NOT be distributed to players.
  Write-Xml (Join-Path $addonSource 'ModABCLG1LeadTest.dll') 'SYNTHETIC_C1_INSTALLER_SENTINEL_NOT_A_DLL'
  $origFiles = @(
    Join-Path $game.db 'Departments.xml'
    Join-Path $game.db 'Diagnoses\DiagnosesER.xml'
    Join-Path $game.db 'Diagnoses\DiagnosesINTERN.xml'
  )
  $hashes = @{}
  foreach($p in $origFiles) { $hashes[$p] = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash }
  & (Join-Path $fixtureInstaller 'Install-ABCL-G1.ps1') -GameRoot $game.root -NativeLeadTest:$nativeLead
  $install = Join-Path $game.addons 'ModABCLG1LeadTest'
  Assert (Test-Path -LiteralPath $install) "$label test install missing"
  $diagnosisDoc = New-Object System.Xml.XmlDocument
  $diagnosisDoc.Load((Join-Path $install 'Database\ModDiagnoses.xml'))
  $rows = @($diagnosisDoc.SelectNodes('/Database/GameDBMedicalCondition'))
  Assert ($rows.Count -eq 2) "$label expected exactly two addon medical condition entries"
  $expectedOriginal = if ($nativeLead) { $leadId } else { 'DIA_CLD' }
  Assert ($null -ne $diagnosisDoc.SelectSingleNode("/Database/GameDBMedicalCondition[@ID='$expectedOriginal']")) "$label original test override missing"
  $private = $diagnosisDoc.SelectSingleNode("/Database/GameDBMedicalCondition[@ID='$caseId']")
  Assert ($null -ne $private) "$label private C1 diagnosis missing"
  Assert ($private.SelectSingleNode('Disabled').InnerText -eq 'true') "$label private disease must be disabled for random pool"
  Assert (@($private.SelectNodes("Examinations/ExaminationRef[text()='$sampleId']")).Count -eq 1) "$label private ABCL sampling must appear exactly once"
  Assert (@($private.SelectNodes('Symptoms/GameDBSymptomRules')).Count -eq 4) "$label mild symptom count mismatch"
  Assert ($null -ne $private.SelectSingleNode('DepartmentRef[text()="DPT_EMERGENCY"]')) "$label expected native ER department"
  Assert (@($private.SelectNodes('Examinations/ExaminationRef[text()="EXM_CBC_TESTING"]')).Count -eq 0) "$label vanilla CBC re-routing"
  $lab = New-Object System.Xml.XmlDocument
  $lab.Load((Join-Path $install 'Database\ModDepartments.xml'))
  Assert (@($lab.SelectNodes('/Database/GameDBDepartment[@ID="DPT_LAB"]/RequiredRoomsClinic/GameDBDepartmentRoomRequirement')).Count -eq 2) "$label native hematology requirement overwritten"
  foreach($p in $origFiles) {
    Assert ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash -eq $hashes[$p]) "$label original game XML changed: $p"
  }
  Assert (@(Get-ChildItem -LiteralPath $game.addons -Directory | Where-Object Name -like '_ABCL_G1_stage_*').Count -eq 0) "$label temporary stage remains after success"
  Write-Host "$label synthetic game XML isolation / private case injection PASS"
}

try {
  New-Item -ItemType Directory -Path $tmpRoot -Force | Out-Null
  Test-Mode $true
  Test-Mode $false
  $collision = New-TestGame 'C1 collision'
  $other = Join-Path $collision.addons 'OtherWorkshopAddon'
  New-Item -ItemType Directory -Path $other -Force | Out-Null
  Write-Xml (Join-Path $other 'ModDiagnoses.xml') "<Database><GameDBMedicalCondition ID='$caseId'/></Database>"
  # Explicit cross-addon ID collision tested with canonical double-quote XML.
  Write-Xml (Join-Path $other 'ModDiagnoses.xml') ('<Database><GameDBMedicalCondition ID="' + $caseId + '"/></Database>')
  $toolDir = Join-Path $tmpRoot 'installer-collision'
  New-Item -ItemType Directory -Path (Join-Path $toolDir 'ModABCLG1LeadTest\Database') -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $repoRoot 'tools\Install-ABCL-G1.ps1') -Destination $toolDir
  Write-Xml (Join-Path $toolDir 'ModABCLG1LeadTest\ModABCLG1LeadTest.dll') 'SYNTHETIC_TEST_SENTINEL_NOT_A_DLL'
  $blocked = $false
  try { & (Join-Path $toolDir 'Install-ABCL-G1.ps1') -GameRoot $collision.root -NativeLeadTest }
  catch { $blocked = $_.Exception.Message -like '*private fixture ID already claimed*' }
  Assert $blocked 'Foreign addon ID conflict did not fail safely'
  Assert (-not (Test-Path -LiteralPath (Join-Path $collision.addons 'ModABCLG1LeadTest'))) 'Collision left a partial ABCL addon'
  Assert (@(Get-ChildItem -LiteralPath $collision.addons -Directory | Where-Object Name -like '_ABCL_G1_stage_*').Count -eq 0) 'Collision left staging remnants'
  Assert (Test-Path -LiteralPath (Join-Path $other 'ModDiagnoses.xml')) 'Foreign addon was altered'
  Write-Host 'C1 other-Mod ID collision / rollback PASS'
  Write-Host 'CLIN001_PRIVATE_FIXTURE_WINDOWS_MOCK=PASS (no real original game files)'
}
finally {
  if (Test-Path -LiteralPath $tmpRoot) {
    Remove-Item -LiteralPath $tmpRoot -Recurse -Force -ErrorAction SilentlyContinue
  }
}
