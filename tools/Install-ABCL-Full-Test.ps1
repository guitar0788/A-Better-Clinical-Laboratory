param([string]$GameRoot, [switch]$Restore)
$ErrorActionPreference = 'Stop'
# Non-destructive integrated test installer. Does not touch vanilla/other mods.
# Before upgrade, validates every file shipped in BUILD_INFO.json. Rollback only
# moves the two known ABCL test-addon directories. Historical backups elsewhere
# are left untouched. Requires disposable test saves.
function Fail([string]$Reason) { throw "ABCL integrated test stopped: $Reason" }
function Need([bool]$Condition, [string]$Reason) { if (!$Condition) { Fail $Reason } }
function Hash([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Is-GameRoot([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    $db = Join-Path $Path 'ProjectHospital_Data\StreamingAssets\Database'
    $mods = Join-Path $Path 'ProjectHospital_Data\StreamingAssets\Addons'
    return (Test-Path -LiteralPath $db -PathType Container) -and
           (Test-Path -LiteralPath $mods -PathType Container)
}
function Discover-Root([string]$Requested) {
    $candidates = @()
    if (![string]::IsNullOrWhiteSpace($Requested)) { $candidates += $Requested }
    $candidates += @('D:\STEAM\steamapps\common\Project Hospital',
                    'C:\Program Files (x86)\Steam\steamapps\common\Project Hospital',
                    'C:\Program Files\Steam\steamapps\common\Project Hospital')
    foreach ($candidate in $candidates) {
        if (![string]::IsNullOrWhiteSpace($candidate) -and (Test-Path -LiteralPath $candidate)) {
            $path = (Resolve-Path -LiteralPath $candidate).Path
            for($i=0; $i -lt 4; $i++) {
                if (Is-GameRoot $path) { return $path.TrimEnd('\') }
                $parent = Split-Path -Parent $path
                if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $path) { break }
                $path = $parent
            }
        }
    }
    $manual=Read-Host 'Enter Project Hospital game folder (containing ProjectHospital_Data)'
    Need (![string]::IsNullOrWhiteSpace($manual)) 'Game folder cannot be empty'
    $path=(Resolve-Path -LiteralPath $manual -ErrorAction Stop).Path
    Need (Is-GameRoot $path) 'Folder is not a verified Project Hospital root'
    return $path.TrimEnd('\')
}
function Check-Owner([string]$Mods,[string]$Name) {
    $target=Join-Path $Mods $Name
    if (!(Test-Path -LiteralPath $target)) { return }
    Need ((Test-Path -LiteralPath $target -PathType Container)) "Existing $Name is not a directory"
    $flags=(Get-Item -LiteralPath $target -Force).Attributes
    Need (-not (($flags -band [IO.FileAttributes]::ReparsePoint) -ne 0)) "Existing $Name is a symlink/junction"
    $file=Join-Path $target 'Database\ModAddon.xml'
    Need (Test-Path -LiteralPath $file -PathType Leaf) "Existing $Name has no owner marker"
    [xml]$xml=Get-Content -LiteralPath $file -Raw
    $expected=if ($Name -eq 'ModABCLG1LeadTest') { 'ADDON_MOD_ABCL_G1_LEAD_TEST' } else { 'ADDON_MOD_ABCL_ART001_PREVIEW' }
    Need ($xml.Database.GameDBAddon.ID -eq $expected) "Existing $Name belongs to unknown addon"
}
function Check-Source([string]$Root, $Info) {
    Need ($Info.schema -eq 'ABCL_OWNER_PINNED_TEST_ONLY_V1') 'Unrecognized test manifest'
    Need ($Info.native_game_L4 -eq 'NOT_RUN') 'Package must not claim gameplay PASS'
    foreach($record in $Info.entries.PSObject.Properties) {
        $entry = [string]$record.Name
        Need ($entry.StartsWith('ModABCLG1LeadTest/') -or
              $entry.StartsWith('ModABCLArt001Test/') -or
              $entry -in @('Install-ABCL-G1.ps1','Install-ABCL-Full-Test.ps1',
                'INSTALL_ABCL_FULL_TEST.cmd','RESTORE_ABCL_FULL_TEST.cmd','README_FIRST_CN.txt')) "Unknown package entry $entry"
        Need (!$entry.Contains('..') -and !$entry.Contains('\')) "Unsafe package entry $entry"
        $file=Join-Path $Root ($entry.Replace('/','\'))
        Need (Test-Path -LiteralPath $file -PathType Leaf) "Required package file missing $entry"
        Need ((Hash $file) -eq ([string]$record.Value).ToLowerInvariant()) "Package file changed $entry"
    }
}
function Check-Installed([string]$Mods,$Info) {
    foreach($record in $Info.entries.PSObject.Properties) {
        $entry=[string]$record.Name
        if (!$entry.StartsWith('ModABCLG1LeadTest/') -and !$entry.StartsWith('ModABCLArt001Test/')) {continue}
        $dst=Join-Path $Mods ($entry.Replace('/','\'))
        if (!(Test-Path -LiteralPath $dst -PathType Leaf)) {return $false}
        if ((Hash $dst) -ne ([string]$record.Value).ToLowerInvariant()) {return $false}
    }
    return $true
}

$here=$PSScriptRoot
$manifestFile=Join-Path $here 'BUILD_INFO.json'
Need (Test-Path -LiteralPath $manifestFile -PathType Leaf) 'BUILD_INFO.json missing'
$manifest=Get-Content -LiteralPath $manifestFile -Raw | ConvertFrom-Json
$game=Discover-Root $GameRoot
# The package and backups must remain outside game data and Workshop scans.
$gameData=(Join-Path $game 'ProjectHospital_Data\StreamingAssets')
Need (!$here.StartsWith($gameData,[StringComparison]::OrdinalIgnoreCase)) 'Extract the full ZIP outside ProjectHospital_Data/StreamingAssets before running'
$mods=Join-Path $game 'ProjectHospital_Data\StreamingAssets\Addons'
$names=@('ModABCLG1LeadTest','ModABCLArt001Test')
if (@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^Project[ ]?Hospital$' }).Count -gt 0) {
    Fail 'Exit Project Hospital before installing/restoring'
}
foreach ($name in $names) {Check-Owner $mods $name}
$marker=Join-Path (Join-Path $mods 'ModABCLG1LeadTest') 'ABCL_FULL_OWNER_MARKER.json'
$statePath=Join-Path $here 'ABCL_INSTALL_STATE.json'
Check-Source $here $manifest

if ($Restore) {
    Need (Test-Path -LiteralPath $statePath -PathType Leaf) 'No installation state in this extracted package'
    $state=Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
    Need ($state.game_root -eq $game) 'This backup belongs to another game location'
    Need (Test-Path -LiteralPath $marker -PathType Leaf) 'Installed ABCL marker missing; no deletion authorized'
    $installed=Get-Content -LiteralPath $marker -Raw | ConvertFrom-Json
    Need ($installed.package_id -eq $state.package_id) 'Installed ABCL does not match this backup'
    Need (Check-Installed $mods $manifest) 'ABCL installed files changed since installation; safe restore blocked'
    foreach($name in @('ModDepartments.xml','ModDiagnoses.xml')) {
        $current=Join-Path (Join-Path $mods 'ModABCLG1LeadTest') ('Database\'+$name)
        $expected=if($name -eq 'ModDepartments.xml'){$state.generated_departments_sha256}else{$state.generated_diagnoses_sha256}
        Need ((Test-Path -LiteralPath $current -PathType Leaf) -and (Hash $current) -eq $expected) "Generated game override changed: $name"
    }
    $backup=Join-Path $here $state.backup_directory
    Need (Test-Path -LiteralPath $backup -PathType Container) 'Backup was moved or deleted'
    foreach($name in $names) {
        Remove-Item -LiteralPath (Join-Path $mods $name) -Recurse -Force
        $saved=Join-Path $backup $name
        if (Test-Path -LiteralPath $saved -PathType Container) {
            Move-Item -LiteralPath $saved -Destination (Join-Path $mods $name)
        }
    }
    Rename-Item -LiteralPath $statePath -NewName ('ABCL_RESTORED_'+[guid]::NewGuid().ToString('N')+'.json')
    Write-Host 'PASS: Only ABCL test addons restored to previous state; all other mods untouched.' -ForegroundColor Green
    return
}

$presentG1=Join-Path $mods 'ModABCLG1LeadTest'
$presentArt=Join-Path $mods 'ModABCLArt001Test'
$packageId=([string]$manifest.compiled_g1_source_sha)+'-'+([string]$manifest.dll_sha256)
if (Test-Path -LiteralPath $marker) {
    $current=Get-Content -LiteralPath $marker -Raw | ConvertFrom-Json
    if ($current.package_id -eq $packageId) {
        Need (Check-Installed $mods $manifest) 'Same-version ABCL installation files changed; refuse to replace unknown modifications'
        $d=Join-Path $presentG1 'Database\ModDepartments.xml'
        $g=Join-Path $presentG1 'Database\ModDiagnoses.xml'
        Need ((Test-Path -LiteralPath $d -PathType Leaf) -and (Test-Path -LiteralPath $g -PathType Leaf)) 'Same package marker but missing generated GameDB overrides'
        Need ((Hash $d) -eq $current.generated_departments_sha256 -and
              (Hash $g) -eq $current.generated_diagnoses_sha256) 'Generated GameDB overrides changed since install; refusing to mask a conflict'
        Write-Host 'ALREADY INSTALLED: same verified ABCL package, no overwrite performed.' -ForegroundColor Green
        return
    }
}
Need (!(Test-Path -LiteralPath $statePath)) 'This extracted test package already has an active backup; use Restore first'
$backupName='_ABCL_OWNER_BACKUP_'+[DateTime]::UtcNow.ToString('yyyyMMddHHmmss')+'_'+[guid]::NewGuid().ToString('N')
$backup=Join-Path $here $backupName
$didMove=@()
$deploymentStarted=$false
try {
    [void](New-Item -ItemType Directory -Path $backup -ErrorAction Stop)
    foreach($name in $names) {
        $src=Join-Path $mods $name
        if (Test-Path -LiteralPath $src) {
            Move-Item -LiteralPath $src -Destination (Join-Path $backup $name) -ErrorAction Stop
            $didMove+= $name
        }
    }
    # Both named old addons have now been moved or were absent: rollback may
    # safely remove only these exact paths, including partial new copies.
    $deploymentStarted=$true
    # Performs the original guarded DPT_LAB + TRM_LDP override from vanilla
    # originals without changing those original files or other addons.
    & (Join-Path $here 'Install-ABCL-G1.ps1') -GameRoot $game -NativeLeadTest
    if (!(Test-Path -LiteralPath $presentG1)) {Fail 'Native guarded G1 installer produced no addon'}
    Copy-Item -LiteralPath (Join-Path $here 'ModABCLArt001Test') -Destination $presentArt -Recurse -ErrorAction Stop
    Need (Check-Installed $mods $manifest) 'Installed resources differ from complete approved manifest'
    $dept=Join-Path $presentG1 'Database\ModDepartments.xml'
    $diag=Join-Path $presentG1 'Database\ModDiagnoses.xml'
    Need ((Test-Path -LiteralPath $dept -PathType Leaf) -and (Test-Path -LiteralPath $diag -PathType Leaf)) 'Native G1 override missing'
    $dynDept=Hash $dept
    $dynDiag=Hash $diag
    $state=@{
        package_id=$packageId;game_root=$game;backup_directory=$backupName;
        generated_departments_sha256=$dynDept;generated_diagnoses_sha256=$dynDiag
    }
    $markerData=@{package_id=$packageId;compiled_source=$manifest.compiled_g1_source_sha;
                  dll_sha256=$manifest.dll_sha256;
                  generated_departments_sha256=$dynDept;generated_diagnoses_sha256=$dynDiag}
    $markerData | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $marker -Encoding UTF8
    $state | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $statePath -Encoding UTF8
    Write-Host 'PASS: ABCL complete integrated test installed and previous ABCL versions safely backed up.' -ForegroundColor Green
    Write-Warning 'Use a disposable save. Room UI, equipment interaction and DLC/Workshop L4 are not yet proven.'
} catch {
    $first=$_.Exception.Message
    # Only remove folders created by THIS invocation, never unknown/other mods.
    foreach($name in $(if($deploymentStarted){$names}else{@()})) {
        $dst=Join-Path $mods $name
        if(Test-Path -LiteralPath $dst) {Remove-Item -LiteralPath $dst -Recurse -Force -ErrorAction SilentlyContinue}
    }
    foreach($name in $didMove) {
        $saved=Join-Path $backup $name
        if(Test-Path -LiteralPath $saved) {
            $dst=Join-Path $mods $name
            if(!(Test-Path -LiteralPath $dst)) {
                Move-Item -LiteralPath $saved -Destination $dst -ErrorAction SilentlyContinue
            }
        }
    }
    Fail "Install did not complete. Prior ABCL backup restoration attempted; $first"
}
