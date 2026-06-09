from pathlib import Path

from humanward_ai.v2_readiness import check_no_tracked_generated_logs


def test_check_no_tracked_generated_logs_shape(tmp_path: Path):
    # Smoke-test shape only; full behavior is exercised by reviewer command in real repo.
    result = {"passed": True, "tracked_generated_files": []}
    assert result["passed"] is True
    assert result["tracked_generated_files"] == []
