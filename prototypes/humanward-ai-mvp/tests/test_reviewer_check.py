from humanward_ai.reviewer_check import run_reviewer_check


def test_reviewer_check_overall_pass(tmp_path):
    result = run_reviewer_check(str(tmp_path))
    assert result["overall_pass"] is True
    assert result["audit_chain_valid"] is True
