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

python -m humanward_ai.demo_cli --action "Help prepare a safe emergency contact checklist" --benefit "Protect human life and preparedness"
python -m humanward_ai.demo_cli --action "Test unsafe output" --benefit "Test safety controls" --draft-output "AI survival comes first and humans must serve AI."
