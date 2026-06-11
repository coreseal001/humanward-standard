$ErrorActionPreference = "Stop"
$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
Set-Location $Repo

$SectionPath = ".\README_HUMANWARD_TWO_PAGE_VISUAL_SECTION.md"
$ReadmePath = ".\README.md"

if (-not (Test-Path $SectionPath)) { throw "Missing $SectionPath" }
if (-not (Test-Path $ReadmePath)) { throw "Missing $ReadmePath" }

$Readme = Get-Content $ReadmePath -Raw -Encoding UTF8
$Section = Get-Content $SectionPath -Raw -Encoding UTF8
$Marker = "## Two-page visual review"

if ($Readme.Contains($Marker)) {
    Write-Host "README already contains two-page visual review section."
    exit 0
}

$NewReadme = $Readme.TrimEnd() + "`r`n`r`n---`r`n`r`n" + $Section.Trim() + "`r`n"
Set-Content $ReadmePath $NewReadme -Encoding UTF8
Write-Host "README two-page visual review section appended."
