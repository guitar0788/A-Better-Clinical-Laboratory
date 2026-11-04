# Test exact BOM-less UTF-8 issue on Windows PowerShell 5.1, not pwsh 7.
# ASCII-only script source: PowerShell 5.1 itself may misdecode BOM-less .ps1.
$ErrorActionPreference='Stop'
if ($PSVersionTable.PSVersion.Major -ne 5) {
  throw 'Expected Windows PowerShell 5.x; test cannot silently use PowerShell 7'
}
$Root=Join-Path $env:RUNNER_TEMP ('ABCL_PS51_UTF8_'+[Guid]::NewGuid().ToString('N'))
New-Item -Path $Root -ItemType Directory -Force | Out-Null
try {
  # U+4E34 U+5E8A U+6BD2 U+7406 U+5B9E U+9A8C U+5BA4:
  # Chinese label for the Toxicology Laboratory, no non-ASCII .ps1 bytes.
  $Label=-join @(
    [char]0x4e34,[char]0x5e8a,[char]0x6bd2,[char]0x7406,
    [char]0x5b9e,[char]0x9a8c,[char]0x5ba4
  )
  $XmlPath=Join-Path $Root 'ModStringTableZhHansTO004.xml'
  $XmlText='<?xml version="1.0" encoding="utf-8"?>'+
    '<Database><GameDBStringTable><LocalizedStrings>'+
    '<GameDBLocalizedString><LocID>PREFAB_ABCL_TO004_TOXICOLOGY_SMALL</LocID><Text>'+
    $Label+'</Text></GameDBLocalizedString>'+
    '<GameDBLocalizedString><LocID>PREFAB_ABCL_TO004_TOXICOLOGY_LARGE</LocID><Text>'+
    $Label+'</Text></GameDBLocalizedString>'+
    '</LocalizedStrings></GameDBStringTable></Database>'
  $Utf8NoBom=New-Object System.Text.UTF8Encoding($false)
  [IO.File]::WriteAllBytes($XmlPath,$Utf8NoBom.GetBytes($XmlText))
  $Raw=[IO.File]::ReadAllBytes($XmlPath)
  if($Raw[0] -eq 239 -and $Raw[1] -eq 187 -and $Raw[2] -eq 191) {
    throw 'Fixture must be UTF8 without BOM to reproduce the owner failure'
  }
  [xml]$Parsed=Get-Content -LiteralPath $XmlPath -Encoding UTF8 -Raw
  $Nodes=@($Parsed.SelectNodes('//GameDBLocalizedString/Text'))
  if($Nodes.Count -ne 2) { throw 'Expected two Chinese localized prefab labels' }
  foreach($Node in $Nodes) {
    if($Node.InnerText -cne $Label) {
      throw 'Explicit UTF8 PowerShell read did not round-trip native Chinese label'
    }
  }
  # The patcher requires all installer and restore text file reads to specify
  # UTF-8, including other XML and JSON and old ABCL ownership manifests.
  $Repo=(Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
  $Patch=Join-Path $Repo 'tools\patch_integrated_r3_utf8.py'
  $Source=Get-Content -LiteralPath $Patch -Encoding UTF8 -Raw
  if(!$Source.Contains('line.replace(" -Raw", " -Encoding UTF8 -Raw")')) {
    throw 'Patcher no longer applies explicit Windows PowerShell 5.1 UTF8 reads'
  }
  if(!$Source.Contains('OUTPUT_SHA256 = "d0f96ecca6f7df1f05cc5b4a29ad56dea145ee2824647d49ecd669670e69b7c2"')) {
    throw 'Reviewed exact output SHA has changed unexpectedly'
  }
  Write-Host 'PASS: Windows PowerShell 5.1 parsed both BOM-less UTF-8 Chinese label entries'
  Write-Host 'PASS: reviewed R3 wrapper patch rule and exact package SHA pin present'
  Write-Host 'GAME_INSTALL_L4=NOT_RUN'
} finally {
  if(Test-Path -LiteralPath $Root) {
    Remove-Item -LiteralPath $Root -Recurse -Force -ErrorAction SilentlyContinue
  }
}
