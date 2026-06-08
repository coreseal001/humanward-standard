# Run this from the extracted HUMANWARD_AI_MVP_BUILD_PACKAGE_2026-06-09 folder.
# Change $Repo if your path is different.

$Repo = "C:\Users\samuel\Desktop\humanward-standard"
$Dest = Join-Path $Repo "prototypes\humanward-ai-mvp"

New-Item -ItemType Directory -Force $Dest | Out-Null
Copy-Item -Recurse -Force .\* $Dest

Set-Location $Repo

# Verify immutable core hash. Must remain unchanged.
Get-FileHash .\core\IMMUTABLE_CORE.md -Algorithm SHA256

git status
git add .\prototypes\humanward-ai-mvp
git commit -m "Add Humanward AI MVP scaffold"
git push origin main
