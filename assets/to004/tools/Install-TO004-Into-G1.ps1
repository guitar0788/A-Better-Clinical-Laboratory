param([string]$GameRoot)
$ErrorActionPreference = 'Stop'
# Additive, disposable-save only: copies precisely eight TO-004 files into an existing G1 test addon.
# This script never edits original StreamingAssets/Database, other addon folders, or save files.
if ([string]::IsNullOrWhiteSpace($GameRoot)) { $GameRoot = Read-Host 'Enter Project Hospital folder containing ProjectHospital_Data' }
$root = (Resolve-Path -LiteralPath $GameRoot -ErrorAction Stop).Path
$addons = Join-Path $root 'ProjectHospital_Data\StreamingAssets\Addons'
$target = Join-Path $addons 'ModABCLG1LeadTest'
$package = Split-Path -Parent $PSScriptRoot
if (!(Test-Path -LiteralPath (Join-Path $root 'ProjectHospital_Data\StreamingAssets\Database') -PathType Container)) { throw 'Not a supported Project Hospital installation root.' }
if (!(Test-Path -LiteralPath $addons -PathType Container)) { throw 'Addons directory not found.' }
if (!(Test-Path -LiteralPath (Join-Path $target 'Database\ModRoomTypes.xml') -PathType Leaf) -or
    !(Test-Path -LiteralPath (Join-Path $target 'Database\ModAddon.xml') -PathType Leaf)) {
    throw 'A complete ABCL G1 test addon must be installed first. No standalone TO-004 install.'
}
$room = [IO.File]::ReadAllText((Join-Path $target 'Database\ModRoomTypes.xml'))
if (!$room.Contains('ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB')) { throw 'Matching G1 toxicology room definition is missing.' }
$names = @(
  'Database\ModAssetListsTO004.xml',
  'Database\ModPrefabObjectsTO004.xml',
  'Database\ModStringTableEnTO004.xml',
  'Database\ModStringTableZhHansTO004.xml',
  'Prefabs\room_toxicology_small.xml',
  'Prefabs\room_toxicology_large.xml',
  'Assets\ABCL\Prefabs\toxicology_small.png',
  'Assets\ABCL\Prefabs\toxicology_large.png'
)
# Perform ALL preflight checks before ANY destination write; never silently overwrite.
foreach ($name in $names) {
  $src = Join-Path $package $name
  $dst = Join-Path $target $name
  if (!(Test-Path -LiteralPath $src -PathType Leaf)) { throw "Missing packaged TO-004 file: $name" }
  if (Test-Path -LiteralPath $dst) { throw "Refusing to overwrite existing file: $name" }
}
$added = New-Object 'System.Collections.Generic.List[string]'
try {
  foreach ($name in $names) {
    $src = Join-Path $package $name
    $dst = Join-Path $target $name
    $parent = Split-Path -Parent $dst
    if (!(Test-Path -LiteralPath $parent -PathType Container)) { [void](New-Item -ItemType Directory -Path $parent -Force) }
    Copy-Item -LiteralPath $src -Destination $dst -ErrorAction Stop
    $added.Add($dst)
    if ((Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash) {
      throw "Checksum mismatch for $name"
    }
  }
  Write-Host 'TO-004 installed: 8 addon-private files added; G1 and vanilla files preserved.' -ForegroundColor Green
  Write-Warning 'Disposable save ONLY. Game-menu, placement, rotation and save/reload L4 still NOT verified.'
} catch {
  foreach ($dst in $added) { if (Test-Path -LiteralPath $dst -PathType Leaf) { Remove-Item -LiteralPath $dst -Force } }
  throw
}