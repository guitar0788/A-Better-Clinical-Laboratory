param([string]$GameRoot)
$ErrorActionPreference = 'Stop'
function Stop-With([string]$message) { throw "ABCL ART-001 stopped: $message" }

if ([string]::IsNullOrWhiteSpace($GameRoot)) {
    $GameRoot = Read-Host 'Enter Project Hospital game root (contains ProjectHospital_Data)'
}
$resolvedGame = (Resolve-Path -LiteralPath $GameRoot).Path
$assets = Join-Path $resolvedGame 'ProjectHospital_Data\StreamingAssets'
$addons = Join-Path $assets 'Addons'
if (!(Test-Path -LiteralPath (Join-Path $resolvedGame 'ProjectHospital_Data') -PathType Container)) {
    Stop-With 'Selected directory is not a Project Hospital game root'
}
if (!(Test-Path -LiteralPath $addons -PathType Container)) {
    Stop-With 'StreamingAssets/Addons was not found'
}

$source = Join-Path $PSScriptRoot 'ModABCLArt001Test'
$target = Join-Path $addons 'ModABCLArt001Test'
if (!(Test-Path -LiteralPath (Join-Path $source 'Database\ModAddon.xml') -PathType Leaf)) {
    Stop-With 'Preview test addon is missing from the package'
}
if (!(Test-Path -LiteralPath (Join-Path $source 'Assets\ABCL\equipment_atlas.png') -PathType Leaf)) {
    Stop-With 'Required equipment atlas is missing'
}
if (!(Test-Path -LiteralPath (Join-Path $source 'Database\ModObjectsABCL.xml') -PathType Leaf)) {
    Stop-With 'Required equipment database XML is missing'
}
if (Test-Path -LiteralPath $target) {
    Stop-With 'Existing ART-001 test folder found. Do not overwrite or upgrade in-place.'
}
$stage = Join-Path $addons 'ModABCLArt001Test.partial'
if (Test-Path -LiteralPath $stage) {
    Stop-With 'An earlier partial test folder exists; stop and inspect it instead of overwriting.'
}

# Copy only ABCL test assets. No game XML, save, DLC, third-party mod or Steam
# files are read or written by this installer.
try {
    Copy-Item -LiteralPath $source -Destination $stage -Recurse -ErrorAction Stop
    if (!(Test-Path -LiteralPath (Join-Path $stage 'Database\ModAddon.xml'))) {
        Stop-With 'Staged addon did not contain its manifest'
    }
    Move-Item -LiteralPath $stage -Destination $target -ErrorAction Stop
} catch {
    # Do not delete a partial file tree automatically; leave it for diagnosis.
    throw
}
Write-Host 'ABCL ART-001 source-only equipment placement test installed.' -ForegroundColor Green
Write-Host 'Not an Alpha release. No test result is implied by installation.'
Write-Host 'Use a NEW disposable save. Do not remove from a save that references the objects.'
