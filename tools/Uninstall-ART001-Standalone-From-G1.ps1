# Scoped removal of a SHA-owned ABCL ART001 TestOnly overlay.
param([Parameter(Mandatory=$true)][string]$GameRoot)
$ErrorActionPreference='Stop'
$Root=[IO.Path]::GetFullPath($GameRoot)
$Addon=Join-Path $Root 'ProjectHospital_Data\StreamingAssets\Addons\ModABCLG1LeadTest'
$Receipt=Join-Path $Addon 'ABCL_ART001_Standalone_TestOnly_Receipt.json'
$Expected=@(
 'Database/ModObjectsABCL.xml',
 'Database/ModAssetListsABCL.xml',
 'Database/ModStringTableEnABCLArt001.xml',
 'Database/ModStringTableZhHansABCLArt001.xml',
 'Assets/ABCL/equipment_atlas.png',
 'Assets/ABCL/icp_ms_icon.png',
 'Assets/ABCL/digestion_station_icon.png'
)
if (!(Test-Path -LiteralPath $Receipt -PathType Leaf)) {
 throw 'No ART001 standalone test receipt found. Nothing removed.'
}
$Record=Get-Content -LiteralPath $Receipt -Raw | ConvertFrom-Json
if ($Record.owner -ne 'ABCL_ART001_Standalone_TestOnly' -or
    $Record.FA_SHA -ne 'cb3a7ab5d03e8677dcb84f486a04bf0ea5f8f622' -or
    $Record.files.Count -ne $Expected.Count) {
 throw 'Not a recognized owned ART001 installation; refusing to remove any files.'
}
$Names=@($Record.files | ForEach-Object {$_.path})
if ((@($Names | Sort-Object -Unique)).Count -ne $Expected.Count) {
 throw 'ART001 receipt has duplicate paths. No removal.'
}
$ToRemove=@()
foreach ($entry in $Record.files) {
 if ($Expected -cnotcontains $entry.path) {
  throw "Refusing non-ART001 receipt path: $($entry.path)"
 }
 $path=Join-Path $Addon ($entry.path.Replace('/','\'))
 if (!(Test-Path -LiteralPath $path -PathType Leaf)) {
  throw "Previously installed ART001 file is missing: $($entry.path)"
 }
 $sha=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
 if ($sha -cne $entry.sha256.ToLowerInvariant()) {
  throw "ART001 file was modified by another addon/user. No automatic deletion: $($entry.path)"
 }
 $ToRemove+= $path
}
foreach ($path in $ToRemove) {
 Remove-Item -LiteralPath $path -Force
}
Remove-Item -LiteralPath $Receipt -Force
Write-Host 'Removed exactly seven owned ART001 test files; G1 and TO004 V3 remain installed.'
Write-Host 'Do not load disposable test hospitals containing removed ART001 equipment!'
