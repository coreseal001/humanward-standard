from pathlib import Path
from humanward_ai.red_team_pack import run_red_team_pack


def test_red_team_pack_passes(tmp_path: Path):
    result = run_red_team_pack(
        audit_log_path=str(tmp_path / "redteam_audit.jsonl"),
        review_queue_path=str(tmp_path / "redteam_review.jsonl"),
    )
    assert result["overall_pass"] is True
    assert result["failed"] == 0
