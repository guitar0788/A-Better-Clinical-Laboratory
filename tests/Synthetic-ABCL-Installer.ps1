# Strictly synthetic Windows deployment test. No original game binary or save.
# Uses temporary fake ProjectHospital_Data and tests only ABCL-namespaced writes.
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Assert([bool]$Value, [string]$Description) {
    if (!$Value) { throw "FAIL: $Description" }
    Write-Host "PASS: $Description"
}
function Put([string]$Path, [string]$Text) {
    $parent=Split-Path -Parent $Path
    if (!(Test-Path -LiteralPath $parent)) {
        [void](New-Item -ItemType Directory -Path $parent -Force)
    }
    [IO.File]::WriteAllText($Path,$Text,[Text.Encoding]::UTF8)
}
function Digest([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
$repoRoot=(Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$root=Join-Path $env:RUNNER_TEMP ('abcl-synthetic-'+[guid]::NewGuid().ToString('N'))
$game=Join-Path $root 'Project Hospital'
$db=Join-Path $game 'ProjectHospital_Data\StreamingAssets\Database'
$mods=Join-Path $game 'ProjectHospital_Data\StreamingAssets\Addons'
[void](New-Item -ItemType Directory -Path $db,$mods -Force)

$department=@'
<Database><GameDBDepartment ID="DPT_LAB"><RequiredRoomsClinic><GameDBDepartmentRoomRequirement><RoomDatabaseEntryRef>ROOM_TYPE_HEMATOLOGY_LAB</RoomDatabaseEntryRef><MinCount>1</MinCount><MaxCount>6</MaxCount></GameDBDepartmentRoomRequirement></RequiredRoomsClinic></GameDBDepartment></Database>
'@
$diagnoses=@'
<Database><GameDBMedicalCondition ID="TRM_LDP"><DepartmentRef>DPT_INTERNAL_MEDICINE_DEPARTMENT</DepartmentRef><Symptoms><GameDBSymptomRules><GameDBSymptomRef>SYM_LEAD_LEVELS_HIGH</GameDBSymptomRef><ProbabilityPercent>100</ProbabilityPercent></GameDBSymptomRules></Symptoms><Treatments><TreatmentRef>TRT_HOSPITALIZATION_HIGH_PRIORITY</TreatmentRef><TreatmentRef>TRT_CHELATION_THERAPY</TreatmentRef></Treatments><Examinations><ExaminationRef>EXM_FAKE_VANILLA</ExaminationRef></Examinations></GameDBMedicalCondition></Database>
'@
Put (Join-Path $db 'Departments.xml') $department
Put (Join-Path $db 'Diagnoses\DiagnosesINTERN.xml') $diagnoses
$deptSHA=Digest (Join-Path $db 'Departments.xml')
$diagSHA=Digest (Join-Path $db 'Diagnoses\DiagnosesINTERN.xml')
$third=Join-Path $mods 'ModThirdPartySafe'
Put (Join-Path $third 'untouched.txt') 'third-party canary - MUST NOT CHANGE'
$thirdSHA=Digest (Join-Path $third 'untouched.txt')

# Older ABCL installations are owned test addons with data to preserve.
$legacyG1=Join-Path $mods 'ModABCLG1LeadTest'
$legacyArt=Join-Path $mods 'ModABCLArt001Test'
Put (Join-Path $legacyG1 'Database\ModAddon.xml') '<Database><GameDBAddon ID="ADDON_MOD_ABCL_G1_LEAD_TEST" /></Database>'
Put (Join-Path $legacyArt 'Database\ModAddon.xml') '<Database><GameDBAddon ID="ADDON_MOD_ABCL_ART001_PREVIEW" /></Database>'
Put (Join-Path $legacyG1 'older-g1.txt') 'Original ABCL G1 saved'
Put (Join-Path $legacyArt 'older-art.txt') 'Original ABCL art saved'
$legacyHash=Digest (Join-Path $legacyG1 'older-g1.txt')

function New-SyntheticPackage([string]$Variant,[bool]$Broken) {
    $package=Join-Path $root ('package-'+$Variant)
    $pkgG1=Join-Path $package 'ModABCLG1LeadTest'
    $pkgArt=Join-Path $package 'ModABCLArt001Test'
    Put (Join-Path $pkgG1 'Database\ModAddon.xml') '<Database><GameDBAddon ID="ADDON_MOD_ABCL_G1_LEAD_TEST" /></Database>'
    Put (Join-Path $pkgArt 'Database\ModAddon.xml') '<Database><GameDBAddon ID="ADDON_MOD_ABCL_ART001_PREVIEW" /></Database>'
    Put (Join-Path $pkgArt 'Assets\ABCL\equipment_atlas.png') ('fixture-equipment-atlas-'+$Variant)
    Put (Join-Path $pkgG1 'Database\ModRoomTypes.xml') '<Database><GameDBRoomType ID="ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB"/></Database>'
    Put (Join-Path $pkgG1 'Database\ModExaminations.xml') '<Database/>'
    Put (Join-Path $pkgG1 'Database\ModStringTableEnABCL.xml') '<Database/>'
    Put (Join-Path $pkgG1 'Database\ModStringTableZhHansABCL.xml') '<Database/>'
    Put (Join-Path $pkgG1 'ModABCLG1LeadTest.dll') ('SYNTHETIC-DLL-NOT-FOR-DISTRIBUTION-'+$Variant)
    Copy-Item -LiteralPath (Join-Path $repoRoot 'tools\Install-ABCL-Full-Test.ps1') -Destination $package -ErrorAction Stop
    if ($Broken) {
        Put (Join-Path $package 'Install-ABCL-G1.ps1') "throw 'Synthetic deliberate failure after backup'"
    } else {
        Copy-Item -LiteralPath (Join-Path $repoRoot 'tools\Install-ABCL-G1.ps1') -Destination $package -ErrorAction Stop
    }
    foreach($name in @('INSTALL_ABCL_FULL_TEST.cmd','RESTORE_ABCL_FULL_TEST.cmd','README_FIRST_CN.txt')) {
        Copy-Item -LiteralPath (Join-Path $repoRoot ('tools\'+$name)) -Destination $package -ErrorAction Stop
    }
    $entries=[ordered]@{}
    foreach($f in @(Get-ChildItem -LiteralPath $package -File -Recurse -Force | Sort-Object FullName)) {
        $relative=$f.FullName.Substring($package.Length+1).Replace('\','/')
        $entries[$relative]=Digest $f.FullName
    }
    $info=[ordered]@{
        schema='ABCL_OWNER_PINNED_TEST_ONLY_V1'
        native_game_L4='NOT_RUN'
        compiled_g1_source_sha='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        dll_sha256='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
        entries=$entries
    }
    $json=$info | ConvertTo-Json -Depth 8
    Put (Join-Path $package 'BUILD_INFO.json') $json
    return $package
}
function Invoke-Install([string]$P,[bool]$Restore) {
    $script=Join-Path $P 'Install-ABCL-Full-Test.ps1'
    if ($Restore) {
        & $script -GameRoot $game -Restore
    } else {
        & $script -GameRoot $game
    }
}
function Check-Canaries([string]$Label) {
    Assert ((Digest (Join-Path $third 'untouched.txt')) -eq $thirdSHA) "$Label third-party Mod unchanged"
    Assert ((Digest (Join-Path $db 'Departments.xml')) -eq $deptSHA) "$Label vanilla department XML unchanged"
    Assert ((Digest (Join-Path $db 'Diagnoses\DiagnosesINTERN.xml')) -eq $diagSHA) "$Label vanilla diagnosis XML unchanged"
}

try {
    $a=New-SyntheticPackage 'A' $false
    Invoke-Install $a $false
    Assert (Test-Path -LiteralPath (Join-Path $a 'ABCL_INSTALL_STATE.json')) 'first install records package state'
    Assert (Test-Path -LiteralPath (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')) 'first install writes owner marker'
    Assert (Test-Path -LiteralPath (Join-Path $legacyG1 'Database\ModDepartments.xml')) 'first install created guarded department override'
    Assert (Test-Path -LiteralPath (Join-Path $legacyG1 'Database\ModDiagnoses.xml')) 'first install created guarded lead override'
    $markerBefore=Digest (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')
    Invoke-Install $a $false
    Assert ((Digest (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')) -eq $markerBefore) 'same-version reinstall is byte-idempotent'
    Check-Canaries 'after first/idempotent install'

    $bad=New-SyntheticPackage 'FAIL' $true
    $caught=$false
    try { Invoke-Install $bad $false } catch { $caught=$true }
    Assert $caught 'synthetic failed upgrade returns error'
    Assert ((Digest (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')) -eq $markerBefore) 'failed upgrade rolls back previous ABCL version'
    Check-Canaries 'after failed upgrade'

    $b=New-SyntheticPackage 'B' $false
    Invoke-Install $b $false
    Assert ((Digest (Join-Path $legacyArt 'Assets\ABCL\equipment_atlas.png')) -eq
             (Digest (Join-Path $b 'ModABCLArt001Test\Assets\ABCL\equipment_atlas.png'))) 'art-only change produces an actual upgrade'
    Assert ((Digest (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')) -ne $markerBefore) 'package identity includes art and XML hashes'
    Check-Canaries 'after upgrade'

    Put (Join-Path $legacyArt 'foreign-file.txt') 'should protect unknown modifications'
    $caught=$false
    try { Invoke-Install $b $true } catch { $caught=$true }
    Assert $caught 'restore blocks unknown files introduced by another addon'
    Assert (Test-Path -LiteralPath (Join-Path $legacyArt 'foreign-file.txt')) 'blocked restore never deletes unknown files'
    Remove-Item -LiteralPath (Join-Path $legacyArt 'foreign-file.txt') -Force

    Invoke-Install $b $true
    Assert ((Digest (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json')) -eq $markerBefore) 'restore newer B returns exact older A'
    Invoke-Install $a $true
    Assert ((Digest (Join-Path $legacyG1 'older-g1.txt')) -eq $legacyHash) 'older owner ABCL G1 restored'
    Assert (Test-Path -LiteralPath (Join-Path $legacyArt 'older-art.txt')) 'older owner ABCL art restored'
    Assert (!(Test-Path -LiteralPath (Join-Path $legacyG1 'ABCL_FULL_OWNER_MARKER.json'))) 'restoration removes only test-installed marker'
    Check-Canaries 'after nested restore'
    Write-Host 'ALL SYNTHETIC INSTALL/UPGRADE/RESTORE CHECKS PASS; NATIVE GAME L4 NOT RUN' -ForegroundColor Green
} finally {
    if (Test-Path -LiteralPath $root) {
        Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
    }
}
