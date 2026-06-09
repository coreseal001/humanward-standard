Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

cd "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard\prototypes\humanward-ai-mvp"

if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    py -3.12 -m venv .venv
}

.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
pip install pytest
python -m pytest
python -m humanward_ai.reviewer_check
python -m humanward_ai.v2_readiness --repo-root "..\.."
