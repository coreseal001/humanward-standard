$ErrorActionPreference = "Stop"

$Repo = "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"
Set-Location $Repo

$Files = @("README.md")
$Files += Get-ChildItem ".\docs" -Recurse -Filter "*.md" | ForEach-Object { $_.FullName }
$Files += Get-ChildItem ".\evidence" -Recurse -Filter "*.md" | ForEach-Object { $_.FullName }

$BadMarkers = @("â", "�", "Ã")
$Failed = $false

foreach ($File in $Files) {
    $Text = Get-Content $File -Raw -Encoding UTF8

    foreach ($Marker in $BadMarkers) {
        if ($Text.Contains($Marker)) {
            Write-Host "Encoding marker found in $File : $Marker"
            $Failed = $true
        }
    }
}

$ReadmeLines = (Get-Content ".\README.md" -Encoding UTF8)
if ($ReadmeLines.Count -lt 80) {
    Write-Host "README line count too low: $($ReadmeLines.Count)"
    $Failed = $true
}

if ($ReadmeLines[0] -ne "# Humanward") {
    Write-Host "README first line is not # Humanward"
    $Failed = $true
}

if ($Failed) {
    throw "Public surface validation failed."
}

Write-Host "Public surface validation passed."
Write-Host "README lines: $($ReadmeLines.Count)"
