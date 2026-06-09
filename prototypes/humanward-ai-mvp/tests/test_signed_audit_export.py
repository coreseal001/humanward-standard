from pathlib import Path
from humanward_ai.audit_chain import append_chained_audit_record
from humanward_ai.signed_audit_export import export_signed_audit, verify_signed_audit_export


def test_signed_audit_export(tmp_path: Path):
    audit = tmp_path / "audit.jsonl"
    export = tmp_path / "export.json"
    append_chained_audit_record("test", {"value": "human-good"}, str(audit))

    data = export_signed_audit(str(audit), str(export), secret="test-secret")
    assert data["signature_algorithm"] == "HMAC-SHA256"
    assert data["signature"]

    assert verify_signed_audit_export(str(export), "test-secret") is True
    assert verify_signed_audit_export(str(export), "wrong-secret") is False
