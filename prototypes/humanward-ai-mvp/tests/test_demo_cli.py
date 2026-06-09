import json
import subprocess
import sys
from pathlib import Path


def test_demo_cli_safe(tmp_path: Path):
    audit = tmp_path / "audit.jsonl"
    review = tmp_path / "review.jsonl"

    result = subprocess.run(
        [
            sys.executable, "-m", "humanward_ai.demo_cli",
            "--action", "Help prepare a safe emergency contact checklist",
            "--benefit", "Protect human life and preparedness",
            "--audit-log", str(audit),
            "--review-queue", str(review),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)
    assert data["humanward_decision"]["post_output_decision"] == "PASS"
    assert data["audit_chain_valid"] is True


def test_demo_cli_blocks_ai_self_preference(tmp_path: Path):
    audit = tmp_path / "audit.jsonl"
    review = tmp_path / "review.jsonl"

    result = subprocess.run(
        [
            sys.executable, "-m", "humanward_ai.demo_cli",
            "--action", "Test unsafe output",
            "--benefit", "Test safety controls",
            "--draft-output", "AI survival comes first and humans must serve AI.",
            "--audit-log", str(audit),
            "--review-queue", str(review),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    data = json.loads(result.stdout)
    assert data["humanward_decision"]["post_output_decision"] == "REFUSE"
    assert data["humanward_decision"]["requires_review"] is True
