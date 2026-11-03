# Test-only ART001 private equipment resource install.
# Requires an existing valid ABCL G1 test addon. Never writes original game data.
param([Parameter(Mandatory=$true)][string]$GameRoot)
$ErrorActionPreference = 'Stop'
$Root = [IO.Path]::GetFullPath($GameRoot)
$Addon = Join-Path $Root 'ProjectHospital_Data\StreamingAssets\Addons\ModABCLG1LeadTest'
$Bundle = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Manifest = Join-Path $Bundle 'ART001_TS_INTEGRATION_MANIFEST.json'
$Receipt = Join-Path $Addon 'ABCL_ART001_Standalone_TestOnly_Receipt.json'
$Expected = @(
  'Database/ModObjectsABCL.xml',
  'Database/ModAssetListsABCL.xml',
  'Database/ModStringTableEnABCLArt001.xml',
  'Database/ModStringTableZhHansABCLArt001.xml',
  'Assets/ABCL/equipment_atlas.png',
  'Assets/ABCL/icp_ms_icon.png',
  'Assets/ABCL/digestion_station_icon.png'
)
function Digest([string]$Path) {
  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function LocalPath([string]$Parent, [string]$Name) {
  if ($Expected -cnotcontains $Name) {
    throw "Unapproved ART001 source path: $Name"
  }
  return Join-Path $Parent ($Name.Replace('/','\'))
}
$Room = Join-Path $Addon 'Database\ModRoomTypes.xml'
$AddonXML = Join-Path $Addon 'Database\ModAddon.xml'
$G1DLL = Join-Path $Addon 'ModABCLG1LeadTest.dll'
if (!(Test-Path -LiteralPath $Room -PathType Leaf) -or
    !(Test-Path -LiteralPath $AddonXML -PathType Leaf) -or
    !(Test-Path -LiteralPath $G1DLL -PathType Leaf)) {
  throw 'A complete compiled G1 test addon must be installed first. ART001 test overlay is not standalone.'
}
$RoomText = [IO.File]::ReadAllText($Room)
if (!$RoomText.Contains('ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB') -or
    !$RoomText.Contains('ui_hematoanalyzer') -or
    !$RoomText.Contains('ui_ria')) {
  throw 'Unknown G1 room ownership or missing original CBC/RIA prerequisites. No ART001 install.'
}
if (Test-Path -LiteralPath $Receipt) {
  throw 'An ART001 test receipt exists: uninstall that test version before installing a new one.'
}
if (!(Test-Path -LiteralPath $Manifest -PathType Leaf)) {
  throw 'The candidate manifest is missing. Do not manually copy files.'
}
$Record = Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json
if ($Record.status -ne 'G1_RESOURCE_OVERLAY_CANDIDATE_L2_ONLY_NOT_INSTALLABLE' -or
    $Record.frozen_FA_sha -ne 'cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622') {
  throw 'Unrecognized source/art approval or revision. No ART001 install.'
}
$Files = $Record.generated_runtime_XML_and_asset_sha256.PSObject.Properties
if ($Files.Count -ne $Expected.Count) {
  throw 'Expected exactly seven additive ART001 GameDB/image files.'
}
foreach ($Entry in $Files) {
  if ($Expected -cnotcontains $Entry.Name) {
    throw "Unapproved additional runtime file: $($Entry.Name)"
  }
  $Src = LocalPath $Bundle $Entry.Name
  $Dst = LocalPath $Addon $Entry.Name
  if (!(Test-Path -LiteralPath $Src -PathType Leaf)) {
    throw "Missing ART001 candidate resource: $($Entry.Name)"
  }
  if ((Digest $Src) -cne $Entry.Value.ToLowerInvariant()) {
    throw "ART001 resource differs from pinned FA stage: $($Entry.Name)"
  }
  if (Test-Path -LiteralPath $Dst) {
    throw "Existing ART001 or third-party file collision: $($Entry.Name). Do not overwrite."
  }
}
$New = @()
try {
  foreach ($Entry in $Files) {
    $Src = LocalPath $Bundle $Entry.Name
    $Dst = LocalPath $Addon $Entry.Name
    $Dir = Split-Path -Parent $Dst
    if (!(Test-Path -LiteralPath $Dir)) {
      New-Item -ItemType Directory -Path $Dir -Force | Out-Null
    }
    Copy-Item -LiteralPath $Src -Destination $Dst -ErrorAction Stop
    $New += @{ path = $Dst; hash = $Entry.Value.ToLowerInvariant() }
    if ((Digest $Dst) -cne $Entry.Value.ToLowerInvariant()) {
      throw "ART001 target corrupted while copying: $($Entry.Name)"
    }
  }
  $receiptObject = [ordered]@{
    owner = 'ABCL_ART001_Standalone_TestOnly'
    FA_SHA = $Record.frozen_FA_sha
    files = $Files | ForEach-Object { [ordered]@{ path = $_.Name; sha256 = $_.Value } }
    old_G1_DLL_SHA256 = (Digest $G1DLL)
    warning = 'Do not load a test save with these new equipment objects after uninstalling this overlay.'
  }
  [IO.File]::WriteAllText($Receipt, ($receiptObject | ConvertTo-Json -Depth 5))
  Write-Host 'ART001 SOURCE-ONLY DEVICE CANDIDATE INSTALLED INTO EXISTING G1 TEST ADDON (7 files).'
  Write-Host 'NOT a proven visual/clinical device; use a disposable hospital only.'
  Write-Host 'TO004 V3 files, G1 DLL and other addons were not replaced.'
}
catch {
  foreach ($Added in $New) {
    if ((Test-Path -LiteralPath $Added.path -PathType Leaf) -and
        (Digest $Added.path) -ceq $Added.hash) {
      Remove-Item -LiteralPath $Added.path -Force
    }
  }
  throw
}
