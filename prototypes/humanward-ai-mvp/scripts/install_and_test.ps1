# Humanward AI MVP install and test
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
pip install pytest
python -m pytest
python -m humanward_ai.cli --action "Help user make a safe emergency checklist" --benefit "Protect human life and preparedness" --data "No personal data" --tool "none" --reversibility "reversible" --confidence "high"
