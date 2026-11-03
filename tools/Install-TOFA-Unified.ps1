param([string]$GameRoot, [switch]$Restore)
$ErrorActionPreference = 'Stop'
# Single-entry TEST-ONLY deployment. No original DB, other Mod or save edits.
# Never runs while Project Hospital is open; original ABCL test addons are
# moved to a reversible, package-local backup before the new build is installed.
function Fail([string]$why) { throw "TO+FA combined test stopped: $why" }
$package = $PSScriptRoot
$infoPath = Join-Path $package 'BUILD_INFO.json'
if (!(Test-Path -LiteralPath $infoPath -PathType Leaf)) { Fail 'BUILD_INFO.json missing' }
$manifest = Get-Content -LiteralPath $infoPath -Raw | ConvertFrom-Json
if ($manifest.stage -ne 'TO+FA SINGLE SESSION TEST-ONLY / NOT A RELEASE') { Fail 'Unexpected package identity' }
if ((Get-Process -ErrorAction SilentlyContinue | Where-Object {
    $_.ProcessName -match '^Project[ ]?Hospital$' }).Count -gt 0) {
    Fail 'Close Project Hospital before installation or restore'
}
if ([string]::IsNullOrWhiteSpace($GameRoot)) {
    $GameRoot = Read-Host 'Enter game root directory (containing ProjectHospital_Data)'
}
$resolved = (Resolve-Path -LiteralPath $GameRoot -ErrorAction Stop).Path.TrimEnd('\')
# Accept a Steam game root OR a previously pasted ProjectHospital_Data/StreamingAssets/Addons subfolder.
for ($i=0; $i -lt 4 -and !(Test-Path -LiteralPath (Join-Path $resolved 'ProjectHospital_Data\StreamingAssets\Database')); $i++) {
    $parent = Split-Path -Parent $resolved
    if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $resolved) { break }
    $resolved = $parent
}
$gameDb = Join-Path $resolved 'ProjectHospital_Data\StreamingAssets\Database'
$addons = Join-Path $resolved 'ProjectHospital_Data\StreamingAssets\Addons'
if (!(Test-Path -LiteralPath $gameDb -PathType Container) -or
    !(Test-Path -LiteralPath $addons -PathType Container)) {
    Fail 'Not the expected Project Hospital game root / StreamingAssets layout'
}
$g1 = 'ModABCLG1LeadTest'
$art = 'ModABCLArt001Test'
$previous = Join-Path $package '_TOFA_PREVIOUS_ABCL_TEST_ONLY'
# Refuse directories that are not clearly the two known ABCL test addons.
function Check-Owned([string]$name) {
    $target = Join-Path $addons $name
    if (!(Test-Path -LiteralPath $target)) { return }
    $addon = Join-Path $target 'Database\ModAddon.xml'
    if (!(Test-Path -LiteralPath $addon -PathType Leaf)) { Fail "Existing folder $name is not a recognized test addon" }
    $identity = [IO.File]::ReadAllText($addon)
    $expected = if ($name -eq $g1) { 'ADDON_MOD_ABCL_G1_LEAD_TEST' } else { 'ADDON_MOD_ABCL_ART001_PREVIEW' }
    if (!$identity.Contains($expected)) { Fail "Unknown owner/identity for existing addon $name" }
}
Check-Owned $g1
Check-Owned $art

if ($Restore) {
    if (!(Test-Path -LiteralPath $previous -PathType Container)) { Fail 'No package-local previous-test backup found' }
    $markerPath = Join-Path (Join-Path $addons $g1) 'TOFA_COMBINED_TEST_SHA.txt'
    if (!(Test-Path -LiteralPath $markerPath)) { Fail 'Current G1 is not marked as this combined package; refuse removal' }
    $marker = [IO.File]::ReadAllText($markerPath).Trim()
    if ($marker -ne $manifest.integration_sha) { Fail 'Current G1 marker differs from package SHA' }
    foreach ($entry in $manifest.entries.PSObject.Properties) {
        if (!$entry.Name.StartsWith("$g1/") -and !$entry.Name.StartsWith("$art/")) { continue }
        $dst = Join-Path $addons ($entry.Name.Replace('/','\'))
        if (!(Test-Path -LiteralPath $dst -PathType Leaf) -or
            (Get-FileHash -LiteralPath $dst -Algorithm SHA256).Hash -ine $entry.Value) {
            Fail "Combined test file has changed; manual review before restore: $($entry.Name)"
        }
    }
    foreach ($name in @($g1,$art)) {
        $dst = Join-Path $addons $name
        if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
        $old = Join-Path $previous $name
        if (Test-Path -LiteralPath $old) { Move-Item -LiteralPath $old -Destination $dst }
    }
    Write-Host 'Combined test removed; original ABCL test folders restored (if previously present).' -ForegroundColor Green
    Write-Warning 'Do not reopen a disposable save containing test-only rooms/devices after removing this package.'
    return
}
if (Test-Path -LiteralPath $previous) { Fail 'Previous backup already exists. Restore first; no second overwrite.' }
# Verify EVERY input byte before touching existing ABCL test folders.
foreach ($entry in $manifest.entries.PSObject.Properties) {
    $src = Join-Path $package $entry.Name.Replace('/','\')
    if (!(Test-Path -LiteralPath $src -PathType Leaf)) { Fail "Missing packaged file: $($entry.Name)" }
    $sha = (Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
    if ($sha -ine $entry.Value) { Fail "Source checksum mismatch: $($entry.Name)" }
}
$backupMade = $false
$installed = $false
try {
    [void](New-Item -ItemType Directory -Path $previous -ErrorAction Stop)
    $backupMade = $true
    foreach ($name in @($g1,$art)) {
        $old = Join-Path $addons $name
        if (Test-Path -LiteralPath $old) { Move-Item -LiteralPath $old -Destination (Join-Path $previous $name) -ErrorAction Stop }
    }
    & (Join-Path $package 'Install-ABCL-G1.ps1') -GameRoot $resolved
    if (!(Test-Path -LiteralPath (Join-Path (Join-Path $addons $g1) 'Database\ModDepartments.xml'))) {
        Fail 'Native G1 addon-local department override missing after install'
    }
    Copy-Item -LiteralPath (Join-Path $package $art) -Destination (Join-Path $addons $art) -Recurse -ErrorAction Stop
    [IO.File]::WriteAllText((Join-Path (Join-Path $addons $g1) 'TOFA_COMBINED_TEST_SHA.txt'), $manifest.integration_sha)
    $installed = $true
    Write-Host 'One combined TO+FA test installation completed. Two ABCL-owned addons installed.' -ForegroundColor Green
    Write-Host 'Previous ABCL-only folders preserved beside this extracted package, never deleted.'
    Write-Warning 'DISPOSABLE SAVE ONLY. L4 visual, graph and gameplay compatibility remain UNVERIFIED.'
}
catch {
    # Transactional rollback, restricted to the exact two named ABCL test folders.
    foreach ($name in @($g1,$art)) {
        $current = Join-Path $addons $name
        if (Test-Path -LiteralPath $current) { Remove-Item -LiteralPath $current -Recurse -Force -ErrorAction SilentlyContinue }
        $old = Join-Path $previous $name
        if (Test-Path -LiteralPath $old) { Move-Item -LiteralPath $old -Destination $current -ErrorAction SilentlyContinue }
    }
    Fail "Installation failed and restoration attempted. Inspect backup before retry. $($_.Exception.Message)"
}
