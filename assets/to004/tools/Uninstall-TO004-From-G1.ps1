param([string]$GameRoot)
$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($GameRoot)) { $GameRoot = Read-Host 'Enter Project Hospital folder containing ProjectHospital_Data' }
$root = (Resolve-Path -LiteralPath $GameRoot -ErrorAction Stop).Path
$target = Join-Path $root 'ProjectHospital_Data\StreamingAssets\Addons\ModABCLG1LeadTest'
$package = Split-Path -Parent $PSScriptRoot
$names = @(
  'Database\ModAssetListsTO004.xml', 'Database\ModPrefabObjectsTO004.xml',
  'Database\ModStringTableEnTO004.xml', 'Database\ModStringTableZhHansTO004.xml',
  'Prefabs\room_toxicology_small.xml', 'Prefabs\room_toxicology_large.xml',
  'Assets\ABCL\Prefabs\toxicology_small.png', 'Assets\ABCL\Prefabs\toxicology_large.png'
)
# Refuse partial uninstalls or removing files edited by the user or another addon.
foreach ($name in $names) {
  $src = Join-Path $package $name
  $dst = Join-Path $target $name
  if (!(Test-Path -LiteralPath $src -PathType Leaf) -or !(Test-Path -LiteralPath $dst -PathType Leaf)) {
    throw "Missing source/installed file; refusal to delete anything: $name"
  }
  if ((Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash) {
    throw "Changed file; refusal to delete anything: $name"
  }
}
foreach ($name in $names) { Remove-Item -LiteralPath (Join-Path $target $name) -Force }
Write-Host 'Removed only the 8 matching TO-004 files; G1 and vanilla files preserved.' -ForegroundColor Green
Write-Warning 'Never reopen a save containing these prefab rooms after removing their definitions.'