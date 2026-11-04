# Synthetic Windows PowerShell installer test. No real game files or saves.
$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\\..')).Path
$tmpRoot = Join-Path $env:RUNNER_TEMP ('g1-r3-isolation-' + [Guid]::NewGuid().ToString('N'))

function Assert([bool] $condition,[string] $reason) {
  if (-not $condition) { throw "G1 R3 installer smoke FAIL: $reason" }
}
function Write-Xml([string] $path,[string] $data) {
  [IO.File]::WriteAllText($path,$data,[System.Text.UTF8Encoding]::new($false))
}
function New-TestGame([string]$label) {
  $root = Join-Path $tmpRoot $label
  $assets = Join-Path $root 'ProjectHospital_Data\\StreamingAssets'
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
  Write-Xml (Join-Path $diagnoses 'DiagnosesINTERN.xml') @'
<Database><GameDBMedicalCondition ID="TRM_LDP">
<DepartmentRef>DPT_INTERNAL_MEDICINE_DEPARTMENT</DepartmentRef>
<Symptoms><GameDBSymptomRules><ProbabilityPercent>100</ProbabilityPercent><GameDBSymptomRef>SYM_LEAD_LEVELS_HIGH</GameDBSymptomRef></GameDBSymptomRules></Symptoms>
<Examinations><ExaminationRef>EXM_INTERVIEW</ExaminationRef></Examinations>
<Treatments><TreatmentRef>TRT_HOSPITALIZATION_HIGH_PRIORITY</TreatmentRef><TreatmentRef>TRT_CHELATION_THERAPY</TreatmentRef></Treatments>
</GameDBMedicalCondition></Database>
'@
  Write-Xml (Join-Path $diagnoses 'DiagnosesER.xml') @'
<Database><GameDBMedicalCondition ID="DIA_CLD"><DepartmentRef>DPT_EMERGENCY</DepartmentRef></GameDBMedicalCondition></Database>
'@
  return @{root=$root;db=$db;diagnoses=$diagnoses;addons=$addons}
}
function Copy-Installer([string]$destination) {
  New-Item -ItemType Directory -Path (Join-Path $destination 'ModABCLG1LeadTest\\Database') -Force | Out-Null
  Copy-Item -LiteralPath (Join-Path $repoRoot 'tools\\Install-ABCL-G1.ps1') -Destination $destination
  # Synthetic sentinel only; never a real DLL or distributable artifact.
  Write-Xml (Join-Path $destination 'ModABCLG1LeadTest\\ModABCLG1LeadTest.dll') 'SYNTHETIC_INSTALLER_TEST_NOT_A_DLL'
}
try {
  New-Item -ItemType Directory -Path $tmpRoot -Force | Out-Null

  # Without the explicit native R3 flag the installer must fail before touching the game.
  $blockedGame = New-TestGame 'no-r3-flag'
  $blockedTools = Join-Path $tmpRoot 'installer-no-flag'
  Copy-Installer $blockedTools
  $blocked = $false
  try { & (Join-Path $blockedTools 'Install-ABCL-G1.ps1') -GameRoot $blockedGame.root }
  catch { $blocked = $_.Exception.Message -like '*supports only the native TRM_LDP route*' }
  Assert $blocked 'Installer accepted a non-R3/default invocation'
  Assert (-not (Test-Path -LiteralPath (Join-Path $blockedGame.addons 'ModABCLG1LeadTest'))) 'No-flag invocation left an addon'

  # Explicit R3 must modify only addon-local copies and preserve vanilla XML.
  $game = New-TestGame 'r3'
  $tools = Join-Path $tmpRoot 'installer-r3'
  Copy-Installer $tools
  $originals = @(
    Join-Path $game.db 'Departments.xml',
    Join-Path $game.diagnoses 'DiagnosesINTERN.xml',
    Join-Path $game.diagnoses 'DiagnosesER.xml'
  )
  $hashes = @{}
  foreach($p in $originals) { $hashes[$p] = (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash }
  & (Join-Path $tools 'Install-ABCL-G1.ps1') -GameRoot $game.root -NativeLeadTest
  $installed = Join-Path $game.addons 'ModABCLG1LeadTest'
  Assert (Test-Path -LiteralPath $installed) 'R3 addon not installed'

  $diagnosis = New-Object System.Xml.XmlDocument
  $diagnosis.Load((Join-Path $installed 'Database\\ModDiagnoses.xml'))
  $rows = @($diagnosis.SelectNodes('/Database/GameDBMedicalCondition'))
  Assert ($rows.Count -eq 1) 'Expected only one addon-local TRM_LDP diagnosis override'
  Assert ($null -ne $diagnosis.SelectSingleNode('/Database/GameDBMedicalCondition[@ID="TRM_LDP"]')) 'Native TRM_LDP override missing'
  Assert (@($diagnosis.SelectNodes('/Database/GameDBMedicalCondition[@ID="TRM_LDP"]/Examinations/ExaminationRef[text()="EXM_ABCL_G1_BLOOD_LEAD_SAMPLING"]')).Count -eq 1) 'ABCL sampling link missing/duplicated'
  Assert ($null -eq $diagnosis.SelectSingleNode('/Database/GameDBMedicalCondition[@ID="DIA_CLD"]')) 'Generic DIA_CLD override must not be generated'
  Assert ($null -eq $diagnosis.SelectSingleNode('/Database/GameDBMedicalCondition[@ID="DIA_ABCL_C1_GM_MILD_LEAD_EXPOSURE"]')) 'Retired C1 fixture must not be generated'

  $lab = New-Object System.Xml.XmlDocument
  $lab.Load((Join-Path $installed 'Database\\ModDepartments.xml'))
  $requirements = @($lab.SelectNodes('/Database/GameDBDepartment[@ID="DPT_LAB"]/RequiredRoomsClinic/GameDBDepartmentRoomRequirement'))
  Assert ($requirements.Count -eq 2) 'Original hematology requirement was not preserved with one additive toxicology room'
  Assert ($null -ne $lab.SelectSingleNode('/Database/GameDBDepartment[@ID="DPT_LAB"]/RequiredRoomsClinic/GameDBDepartmentRoomRequirement[RoomDatabaseEntryRef="ROOM_TYPE_HEMATOLOGY_LAB" and MinCount="1"]')) 'Original mandatory hematology room was changed'

  foreach($p in $originals) {
    Assert ((Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash -eq $hashes[$p]) "Original game XML changed: $p"
  }
  Assert (@(Get-ChildItem -LiteralPath $game.addons -Directory | Where-Object Name -like '_ABCL_G1_stage_*').Count -eq 0) 'Temporary stage remains after success'
  Write-Host 'G1 R3 synthetic installer isolation PASS (only TRM_LDP override; no C1/DIA_CLD)'

  Write-Host 'G1_R3_INSTALLER_ISOLATION=PASS (synthetic XML only; no real game L4)'
}
finally {
  if (Test-Path -LiteralPath $tmpRoot) {
    Remove-Item -LiteralPath $tmpRoot -Recurse -Force -ErrorAction SilentlyContinue
  }
}
