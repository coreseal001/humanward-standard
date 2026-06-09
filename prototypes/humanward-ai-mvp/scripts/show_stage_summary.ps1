cd "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard"

Write-Host "== Git =="
git log --oneline -8
git status

Write-Host ""
Write-Host "== Immutable core =="
Get-FileHash .\core\IMMUTABLE_CORE.md -Algorithm SHA256

Write-Host ""
Write-Host "== Tags =="
git tag --list "humanward-public-v*"

Write-Host ""
Write-Host "== MVP tests =="
cd .\prototypes\humanward-ai-mvp
python -m pytest

Write-Host ""
Write-Host "== Reviewer check =="
python -m humanward_ai.reviewer_check

Write-Host ""
Write-Host "== V2 readiness =="
python -m humanward_ai.v2_readiness --repo-root "..\.."
