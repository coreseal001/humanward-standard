$ErrorActionPreference = "Stop"

$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
$SectionPath = Join-Path $Repo "README_HUMANWARD_V2_MANDATE_SECTION.md"
$ReadmePath = Join-Path $Repo "README.md"
$BackupPath = Join-Path $Repo "README.before-v2-mandate.bak.md"

if (-not (Test-Path $SectionPath)) { throw "Missing section file: $SectionPath" }
if (-not (Test-Path $ReadmePath)) { throw "Missing README.md: $ReadmePath" }

$Readme = Get-Content $ReadmePath -Raw
$Section = Get-Content $SectionPath -Raw

if ($Readme -match "HUMANWARD_V2_MANDATE_START") {
    Write-Host "README already contains Humanward v2 mandate section. No change made."
    exit 0
}

Copy-Item $ReadmePath $BackupPath -Force
$Updated = $Section + "`r`n" + $Readme
Set-Content $ReadmePath $Updated -Encoding UTF8
Write-Host "README updated."
Write-Host "Backup created: $BackupPath"
