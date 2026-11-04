# Source-only Windows L2 smoke fixture. NEVER points to any real Project Hospital installation.
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..\..')).Path
$addonRoot = Join-Path $repo 'assets\to004'
$installScript = Join-Path $addonRoot 'tools\Install-TO004-Into-G1.ps1'
$uninstallScript = Join-Path $addonRoot 'tools\Uninstall-TO004-From-G1.ps1'
if (!(Test-Path -LiteralPath $installScript -PathType Leaf)) { throw 'Installer missing' }
if (!(Test-Path -LiteralPath $uninstallScript -PathType Leaf)) { throw 'Uninstaller missing' }
$sourceRoot = Join-Path $env:RUNNER_TEMP ('abcl-to004-smoke-' + [guid]::NewGuid().ToString('N'))
if (!(Test-Path -LiteralPath $env:RUNNER_TEMP -PathType Container)) { throw 'Must run on a Windows GitHub runner with RUNNER_TEMP set' }
$stAssets = Join-Path $sourceRoot 'ProjectHospital_Data\StreamingAssets'
$gameDb = Join-Path $stAssets 'Database'
$target = Join-Path $stAssets 'Addons\ModABCLG1LeadTest'
$g1Db = Join-Path $target 'Database'
$names = @(
  'Database\ModAssetListsTO004.xml','Database\ModPrefabObjectsTO004.xml',
  'Database\ModStringTableEnTO004.xml','Database\ModStringTableZhHansTO004.xml',
  'Prefabs\room_toxicology_small.xml','Prefabs\room_toxicology_large.xml',
  'Assets\ABCL\Prefabs\toxicology_small.png','Assets\ABCL\Prefabs\toxicology_large.png'
)
function Expect-Refusal([scriptblock]$op, [string]$label) {
    $failed=$false
    try { & $op } catch { $failed=$true }
    if (!$failed) { throw "$label unexpectedly succeeded" }
}
try {
    New-Item -ItemType Directory -Path $gameDb,$g1Db -Force | Out-Null
    Set-Content -LiteralPath (Join-Path $g1Db 'ModAddon.xml') -Value '<Database><GameDBAddon ID="ADDON_MOD_ABCL_G1_LEAD_TEST" /></Database>' -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $g1Db 'ModRoomTypes.xml') -Value '<Database><GameDBRoomType ID="ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB" /></Database>' -Encoding UTF8
    $original = Join-Path $gameDb 'DO_NOT_TOUCH.xml'
    Set-Content -LiteralPath $original -Value '<Database><ORIGINAL /></Database>' -Encoding UTF8
    $hash=(Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash

    # Initial install has exactly 8 files, preserving existing G1/vanilla files.
    & $installScript -GameRoot $sourceRoot
    foreach($name in $names) {
        $actual=Join-Path $target $name
        $expected=Join-Path $addonRoot $name
        if (!(Test-Path -LiteralPath $actual -PathType Leaf)) { throw "Expected installed file missing: $name" }
        if ((Get-FileHash $actual -Algorithm SHA256).Hash -ne (Get-FileHash $expected -Algorithm SHA256).Hash) { throw "Hash differs: $name" }
    }
    Expect-Refusal { & $installScript -GameRoot $sourceRoot } 'Duplicate installation'

    # Tamper one installed file, confirm uninstaller refuses to remove ANY file.
    $tampered=Join-Path $target 'Database\ModPrefabObjectsTO004.xml'
    Add-Content -LiteralPath $tampered -Value '<!-- deliberately changed -->'
    Expect-Refusal { & $uninstallScript -GameRoot $sourceRoot } 'Modified package removal'
    foreach($name in $names) { if (!(Test-Path (Join-Path $target $name) -PathType Leaf)) { throw 'Partial uninstall occurred' } }
    Copy-Item -LiteralPath (Join-Path $addonRoot 'Database\ModPrefabObjectsTO004.xml') -Destination $tampered -Force

    # Clean uninstall removes only the eight TO-004 files.
    & $uninstallScript -GameRoot $sourceRoot
    foreach($name in $names) { if (Test-Path (Join-Path $target $name)) { throw "Not removed: $name" } }
    if (!(Test-Path -LiteralPath (Join-Path $g1Db 'ModRoomTypes.xml') -PathType Leaf)) { throw 'Existing G1 room was removed' }
    if ((Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash -ne $hash) { throw 'Vanilla fixture was modified' }
    Expect-Refusal { & $uninstallScript -GameRoot $sourceRoot } 'Duplicate removal'

    # Missing G1 room definition refuses to install.
    Remove-Item -LiteralPath (Join-Path $g1Db 'ModRoomTypes.xml') -Force
    Expect-Refusal { & $installScript -GameRoot $sourceRoot } 'G1 missing room ID'
    foreach($name in $names) { if (Test-Path (Join-Path $target $name)) { throw 'Failed prerequisite still wrote files' } }
    Write-Host 'TO-004 Windows L2 smoke PASS: install, hashes, refusal, tamper guard, uninstall, prerequisite guard and vanilla preservation.'
} finally {
    if (Test-Path -LiteralPath $sourceRoot) { Remove-Item -LiteralPath $sourceRoot -Recurse -Force }
}