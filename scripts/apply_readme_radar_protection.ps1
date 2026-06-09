$ErrorActionPreference = "Stop"

$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
$SectionPath = Join-Path $Repo "README_HUMANWARD_RADAR_PROTECTION_SECTION.md"
$ReadmePath = Join-Path $Repo "README.md"

if (-not (Test-Path $SectionPath)) { throw "Missing section file: $SectionPath" }
if (-not (Test-Path $ReadmePath)) { throw "Missing README.md: $ReadmePath" }

$Readme = Get-Content $ReadmePath -Raw
$Section = Get-Content $SectionPath -Raw

if ($Readme -match "HUMANWARD_RADAR_PROTECTION_START") {
    Write-Host "README already contains radar/protection section. No change made."
    exit 0
}

$Updated = $Section + "`r`n" + $Readme
Set-Content $ReadmePath $Updated -Encoding UTF8
Write-Host "README updated with radar/protection section."
