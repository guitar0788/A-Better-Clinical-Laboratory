# ABCL integrated R3 restore synthetic Windows test. NEVER uses the real game.
$ErrorActionPreference='Stop'
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$Restore=Join-Path $Repo 'tools\Restore-ABCL-Previous.ps1'
$Root=Join-Path $env:RUNNER_TEMP ('ABCLRollback_'+[Guid]::NewGuid().ToString('N'))
$Owner='ABCL-G1-ART001-TO001-TO004-INTEGRATED-TESTONLY-20261104-R3'
function Check([bool]$Ok,[string]$ErrorText) { if (!$Ok) { throw "Restore smoke FAIL: $ErrorText" } }
function Hash([string]$File) { (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() }
function Fixture([string]$Case,[bool]$WithOld) {
  $Game=Join-Path $Root $Case
  $Addons=Join-Path $Game 'ProjectHospital_Data\StreamingAssets\Addons'
  $Target=Join-Path $Addons 'ModABCLG1LeadTest'
  $Other=Join-Path $Addons 'UnrelatedWorkshop'
  $Backups=Join-Path $Game 'ABCL_Test_Backups'
  New-Item -ItemType Directory -Path $Target,$Other,$Backups -Force | Out-Null
  [IO.File]::WriteAllText((Join-Path $Other 'marker.txt'),'DO NOT ALTER')
  $Managed=@()
  for($i=0;$i -lt 24;$i++) {
    $Rel=('Assets\ABCL\mock{0:D2}.png' -f $i)
    $File=Join-Path $Target $Rel
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $File) | Out-Null
    [IO.File]::WriteAllText($File,('fake owner-only asset '+$i))
    $Managed+=@{path=$Rel.Replace('\','/');sha256=(Hash $File)}
  }
  $Generated=@()
  foreach($Name in @('ModDepartments.xml','ModDiagnoses.xml')) {
    $Rel='Database\'+$Name
    $File=Join-Path $Target $Rel
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $File) | Out-Null
    [IO.File]::WriteAllText($File,'<Database><MockOnly /></Database>')
    $Generated+=@{path=$Rel;sha256=(Hash $File)}
  }
  $Previous=''
  if($WithOld) {
    $Previous=Join-Path $Backups ('ModABCLG1LeadTest_'+'a'*32)
    New-Item -ItemType Directory -Path (Join-Path $Previous 'Database') -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $Previous 'Database\ModAddon.xml'),
      '<Database><GameDBAddon ID="ADDON_MOD_ABCL_G1_LEAD_TEST"/></Database>')
    [IO.File]::WriteAllText((Join-Path $Previous 'ModABCLG1LeadTest.dll'),'PREVIOUS_OWNER_ONLY_VERSION')
  }
  $Receipt=[ordered]@{
    owner=$Owner
    previous_addon_backup=$Previous
    managed_files=$Managed
    generated_files=$Generated
  }
  $Receipt | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $Target 'ABCL_INTEGRATED_TEST_RECEIPT.json') -Encoding utf8
  return @{Game=$Game;Target=$Target;Previous=$Previous;Addons=$Addons;Other=$Other}
}
function AssertOther($F) {
  Check ((Get-Content -LiteralPath (Join-Path $F.Other 'marker.txt') -Raw) -eq 'DO NOT ALTER') 'Third-party Workshop addon was modified'
}
function ExpectRefusal($F,[string]$Expected) {
  $Failed=$false
  try { & $Restore -GameRoot $F.Game }
  catch { $Failed=$_.Exception.Message.Contains($Expected) }
  Check $Failed "Expected protective refusal: $Expected"
  Check (Test-Path -LiteralPath $F.Target) 'Refusal unexpectedly moved live ABCL'
  AssertOther $F
}
try {
  New-Item -ItemType Directory -Path $Root -Force | Out-Null
  $f=Fixture 'restore-valid-old' $true
  & $Restore -GameRoot $f.Game
  Check (Test-Path -LiteralPath (Join-Path $f.Target 'ModABCLG1LeadTest.dll')) 'Prior ABCL DLL not restored'
  Check ((Get-Content (Join-Path $f.Target 'ModABCLG1LeadTest.dll')) -eq 'PREVIOUS_OWNER_ONLY_VERSION') 'Wrong ABCL version after restore'
  Check (@(Get-ChildItem (Join-Path $f.Game 'ABCL_Test_Backups') -Directory -Filter 'Retired_Integrated_Test_*').Count -eq 1) 'Test addon not preserved outside Addons'
  AssertOther $f
  Write-Host 'PASS: valid receipt -> old ABCL restored, current test retained, Workshop unaffected'

  $f=Fixture 'restore-no-previous' $false
  & $Restore -GameRoot $f.Game
  Check (!(Test-Path -LiteralPath $f.Target)) 'Test candidate remained active without previous backup'
  Check (@(Get-ChildItem (Join-Path $f.Game 'ABCL_Test_Backups') -Directory -Filter 'Retired_Integrated_Test_*').Count -eq 1) 'Test candidate was lost'
  AssertOther $f
  Write-Host 'PASS: no previous version -> test addon retired, unrelated Workshop unaffected'

  $f=Fixture 'refuse-missing-backup' $true
  Remove-Item -LiteralPath $f.Previous -Recurse -Force
  ExpectRefusal $f 'Previous ABCL test backup not found'
  Write-Host 'PASS: missing previous backup fails BEFORE moving active addon'

  $f=Fixture 'refuse-manifest-owner' $true
  $path=Join-Path $f.Target 'ABCL_INTEGRATED_TEST_RECEIPT.json'
  $r=Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
  $r.owner='ABCL-UNKNOWN-OLD-RECEIPT'
  $r | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $path
  ExpectRefusal $f 'Receipt does not belong'
  Write-Host 'PASS: unexpected package owner fails closed'

  $f=Fixture 'refuse-tampered-file' $true
  [IO.File]::AppendAllText((Join-Path $f.Target 'Assets\ABCL\mock00.png'),'TAMPER')
  ExpectRefusal $f 'Owned test file was changed'
  Write-Host 'PASS: tampered managed file fails BEFORE moving active addon'

  Write-Host 'INTEGRATED_RESTORE_WINDOWS_SYNTHETIC=PASS; game L4 and ordinary-save safety NOT TESTED'
} finally {
  if (Test-Path -LiteralPath $Root) { Remove-Item -LiteralPath $Root -Force -Recurse -ErrorAction SilentlyContinue }
}
