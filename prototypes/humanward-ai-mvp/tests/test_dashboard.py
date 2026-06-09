from humanward_ai.dashboard import render_dashboard


def test_dashboard_renders_empty_state(tmp_path):
    html = render_dashboard(str(tmp_path / "audit.jsonl"), str(tmp_path / "review.jsonl"))
    assert "Humanward Local Audit Dashboard" in html
    assert "No audit records found" in html
    assert "No review records found" in html
