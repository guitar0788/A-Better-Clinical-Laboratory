param([string]$GameRoot, [switch]$NativeLeadReviewOnly)
$ErrorActionPreference = 'Stop'
function Stop-With([string]$reason) { throw "ABCL G1 stopped: $reason" }
function OriginalEntry($doc,[string]$kind,[string]$entryId) {
  $xpath = "//" + $kind + "[@ID='" + $entryId + "']"
  $nodes = @($doc.SelectNodes($xpath))
  if ($nodes.Count -ne 1) { Stop-With "Expected one original $entryId; found $($nodes.Count)." }
  return $nodes[0]
}
function Add-Text($doc,$parent,[string]$tag,[string]$text) {
  $node = $doc.CreateElement($tag)
  $node.InnerText = $text
  [void]$parent.AppendChild($node)
}
function Make-Override([string]$source,[string]$kind,[string]$id,[string]$destination,[string]$newExamination,[bool]$isRoom) {
  if (!(Test-Path -LiteralPath $source)) { Stop-With "Original game XML missing: $source" }
  $original = New-Object System.Xml.XmlDocument
  $original.Load($source)
  $entry = OriginalEntry $original $kind $id
  $out = New-Object System.Xml.XmlDocument
  [void]$out.AppendChild($out.CreateXmlDeclaration('1.0','utf-8',$null))
  $root = $out.CreateElement('Database')
  [void]$out.AppendChild($root)
  $copy = $out.ImportNode($entry,$true)
  [void]$root.AppendChild($copy)
  if ($isRoom) {
    $required = $copy.SelectSingleNode('RequiredRoomsClinic')
    if ($null -eq $required) { Stop-With 'DPT_LAB has no RequiredRoomsClinic' }
    $mandatory = @($required.SelectNodes("GameDBDepartmentRoomRequirement[RoomDatabaseEntryRef='ROOM_TYPE_HEMATOLOGY_LAB']"))
    if ($mandatory.Count -ne 1 -or [int]$mandatory[0].SelectSingleNode('MinCount').InnerText -lt 1) {
      Stop-With 'Mandatory original hematology lab requirement changed'
    }
    if ($required.SelectSingleNode("GameDBDepartmentRoomRequirement[RoomDatabaseEntryRef='ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB']")) { Stop-With 'ABCL G1 room already present' }
    $room = $out.CreateElement('GameDBDepartmentRoomRequirement')
    Add-Text $out $room 'RoomDatabaseEntryRef' 'ROOM_TYPE_ABCL_G1_TOXICOLOGY_LAB'
    Add-Text $out $room 'MinCount' '0'
    Add-Text $out $room 'MaxCount' '5'
    [void]$required.AppendChild($room)
  } else {
    if ($id -eq 'TRM_LDP') {
      if ($copy.SelectSingleNode('DepartmentRef').InnerText -ne 'DPT_INTERNAL_MEDICINE_DEPARTMENT') { Stop-With 'Unexpected lead case department' }
      $lead = @($copy.SelectNodes("Symptoms/GameDBSymptomRules[GameDBSymptomRef='SYM_LEAD_LEVELS_HIGH' and ProbabilityPercent='100']"))
      if ($lead.Count -ne 1) { Stop-With 'Original lead symptom probability changed' }
      foreach ($t in @('TRT_HOSPITALIZATION_HIGH_PRIORITY','TRT_CHELATION_THERAPY')) {
        if (!$copy.SelectSingleNode("Treatments/TreatmentRef[text()='$t']")) { Stop-With "Missing original treatment $t" }
      }
    }
    $exams = $copy.SelectSingleNode('Examinations')
    if ($null -eq $exams) { Stop-With "Missing Examinations in $id" }
    foreach ($exam in @($exams.SelectNodes('ExaminationRef'))) {
      if ($exam.InnerText -eq $newExamination) { Stop-With "Examination already added to $id" }
    }
    Add-Text $out $exams 'ExaminationRef' $newExamination
  }
  $out.Save($destination)
}
if ([string]::IsNullOrWhiteSpace($GameRoot)) {
  $GameRoot = Read-Host 'Enter game root directory (containing ProjectHospital_Data)'
}
$gameRootFull = (Resolve-Path -LiteralPath $GameRoot).Path
$assets = Join-Path $gameRootFull 'ProjectHospital_Data\StreamingAssets'
if (!(Test-Path -LiteralPath $assets)) { Stop-With 'StreamingAssets not found in selected game directory' }
$db = Join-Path $assets 'Database'
$addons = Join-Path $assets 'Addons'
$target = Join-Path $addons 'ModABCLG1LeadTest'
if (Test-Path -LiteralPath $target) { Stop-With 'Existing G1 folder detected; refusal to overwrite' }
foreach ($old in @('ModABCLPreflight','ModABCLG1ForceLeadEvent')) {
  if (Test-Path -LiteralPath (Join-Path $addons $old)) { Stop-With "Conflicting test addon $old installed" }
}
$sourceAddon = Join-Path $PSScriptRoot 'ModABCLG1LeadTest'
if (!(Test-Path -LiteralPath (Join-Path $sourceAddon 'ModABCLG1LeadTest.dll'))) { Stop-With 'Compiled panel DLL missing' }
$stage = Join-Path $addons ('_ABCL_G1_stage_' + [guid]::NewGuid().ToString('N'))
try {
  Copy-Item -LiteralPath $sourceAddon -Destination $stage -Recurse -Force
  $outDb = Join-Path $stage 'Database'
  Make-Override (Join-Path $db 'Departments.xml') 'GameDBDepartment' 'DPT_LAB' (Join-Path $outDb 'ModDepartments.xml') '' $true
  if ($NativeLeadReviewOnly) {
    # R3: Addon-local clinical association only. Does NOT prove admission or treatment.
    Make-Override (Join-Path $db 'Diagnoses\DiagnosesINTERN.xml') 'GameDBMedicalCondition' 'TRM_LDP' (Join-Path $outDb 'ModDiagnoses.xml') 'EXM_ABCL_G1_BLOOD_LEAD_SAMPLING' $false
  } else {
    # Previously accepted R2 disposable clinic fixture is still the default.
    Make-Override (Join-Path $db 'Diagnoses\DiagnosesER.xml') 'GameDBMedicalCondition' 'DIA_CLD' (Join-Path $outDb 'ModDiagnoses.xml') 'EXM_ABCL_G1_BLOOD_LEAD_SAMPLING' $false
  }
  Move-Item -LiteralPath $stage -Destination $target
  if ($NativeLeadReviewOnly) {
    Write-Warning 'R3 native lead disease association staged for OFFLINE REVIEW only. R2 panel is not a native lead patient generator; do not use for gameplay acceptance.'
  } else {
    Write-Host 'R2 lab-only test installed. DIA_CLD override inside addon only; original game files unchanged. Disposable save ONLY.' -ForegroundColor Green
  }
} catch {
  if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
  throw
}
