# ABCL R3 integrated test: fail-closed, verified rollback of this package only.
# Original game XML and unrelated addons are never modified.
param([string]$GameRoot)
$ErrorActionPreference = 'Stop'
function Fail([string]$Message) { throw "ABCL integrated restore refused: $Message" }
function Digest([string]$File) { (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() }
if ([string]::IsNullOrWhiteSpace($GameRoot)) {
  $GameRoot=Read-Host 'Enter Project Hospital game root (contains ProjectHospital_Data)'
}
if (!(Test-Path -LiteralPath $GameRoot -PathType Container)) { Fail 'Selected game root not found; no files moved' }
$GameRoot=(Resolve-Path -LiteralPath $GameRoot).Path
$Target=Join-Path $GameRoot 'ProjectHospital_Data\StreamingAssets\Addons\ModABCLG1LeadTest'
$Receipt=Join-Path $Target 'ABCL_INTEGRATED_TEST_RECEIPT.json'
if (!(Test-Path -LiteralPath $Receipt -PathType Leaf)) { Fail 'No integrated-test installation receipt; no files moved' }
$R=Get-Content -LiteralPath $Receipt -Raw | ConvertFrom-Json
$PackageId='ABCL-G1-ART001-TO001-TO004-INTEGRATED-TESTONLY-20261104-R3'
if ($R.owner -cne $PackageId) { Fail 'Receipt does not belong to this exact integrated-test package; no files moved' }
if (@($R.managed_files).Count -lt 24 -or @($R.managed_files).Count -gt 60 -or
    @($R.generated_files).Count -ne 2) { Fail 'Unexpected receipt inventory size; no files moved' }
$Seen=New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
foreach ($Entry in @($R.managed_files) + @($R.generated_files)) {
  $Name=[string]$Entry.path
  $Expected=[string]$Entry.sha256
  if ([string]::IsNullOrWhiteSpace($Name) -or $Name.Contains('..') -or
      $Name.Contains(':') -or $Name.StartsWith('/') -or $Name.StartsWith('\') -or
      $Name -notmatch '^[a-zA-Z0-9_\-.\\/]+$') { Fail "Unsafe receipt path '$Name'; no files moved" }
  if (!$Seen.Add($Name.Replace('/','\'))) { Fail "Duplicate receipt path '$Name'; no files moved" }
  if ($Expected -cnotmatch '^[0-9a-f]{64}$') { Fail "Invalid checksum receipt '$Name'; no files moved" }
  $File=Join-Path $Target ($Name.Replace('/','\'))
  if (!(Test-Path -LiteralPath $File -PathType Leaf)) { Fail "Owned test file missing '$Name'; no files moved" }
  if ((Digest $File) -cne $Expected) { Fail "Owned test file was changed '$Name'; no files moved" }
}
$ExpectedGenerated=@('Database\ModDepartments.xml', 'Database\ModDiagnoses.xml')
foreach($Name in $ExpectedGenerated) {
  if (!$Seen.Contains($Name)) { Fail "Missing controlled native override '$Name'; no files moved" }
}
$BackupDir=Join-Path $GameRoot 'ABCL_Test_Backups'
$Previous=[string]$R.previous_addon_backup
if (![string]::IsNullOrWhiteSpace($Previous)) {
  $Previous=[IO.Path]::GetFullPath($Previous)
  $Parent=[IO.Path]::GetFullPath((Split-Path -Parent $Previous))
  $AllowedParent=[IO.Path]::GetFullPath($BackupDir)
  $Leaf=Split-Path -Leaf $Previous
  if ($Parent -cne $AllowedParent -and $Parent -ine $AllowedParent) {
    Fail 'Previous backup is outside the game-root ABCL_Test_Backups folder; no files moved'
  }
  if ($Leaf -notmatch '^ModABCLG1LeadTest_[0-9a-fA-F]{32}$' -or
      !(Test-Path -LiteralPath $Previous -PathType Container)) {
    Fail 'Previous ABCL test backup not found or has unexpected name; no files moved'
  }
  $OldAddon=Join-Path $Previous 'Database\ModAddon.xml'
  $OldDll=Join-Path $Previous 'ModABCLG1LeadTest.dll'
  if (!(Test-Path -LiteralPath $OldAddon -PathType Leaf) -or
      !(Test-Path -LiteralPath $OldDll -PathType Leaf)) {
    Fail 'Previous backup incomplete; no files moved'
  }
  [xml]$OldXml=Get-Content -LiteralPath $OldAddon -Raw
  if ($OldXml.Database.GameDBAddon.ID -ne 'ADDON_MOD_ABCL_G1_LEAD_TEST') {
    Fail 'Previous backup is not owned by the ABCL G1 test; no files moved'
  }
}
# A previous addon is validated before moving the currently installed one.
New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
$Retired=Join-Path $BackupDir ('Retired_Integrated_Test_'+[guid]::NewGuid().ToString('N'))
Move-Item -LiteralPath $Target -Destination $Retired -ErrorAction Stop
try {
  if (![string]::IsNullOrWhiteSpace($Previous)) {
    Move-Item -LiteralPath $Previous -Destination $Target -ErrorAction Stop
    if (!(Test-Path -LiteralPath (Join-Path $Target 'ModABCLG1LeadTest.dll') -PathType Leaf)) {
      Fail 'Restored test DLL not found after move'
    }
    Write-Host 'RESTORE PASS: previous ABCL test addon returned; the retired candidate was preserved.'
  } else {
    Write-Host 'RESTORE PASS: no old ABCL addon existed; test candidate retired outside Addons.'
  }
  Write-Host "Retired candidate backup: $Retired"
} catch {
  $RestoreError=$_
  if (!(Test-Path -LiteralPath $Target) -and (Test-Path -LiteralPath $Retired)) {
    try { Move-Item -LiteralPath $Retired -Destination $Target -ErrorAction Stop }
    catch { Write-Warning "Rollback of the interrupted restore failed; preserve $Retired and recover manually: $_" }
  }
  throw $RestoreError
}
Write-Warning 'Do not reopen a temporary hospital save whose ABCL machines/room definitions were removed.'
