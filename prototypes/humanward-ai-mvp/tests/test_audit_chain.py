from pathlib import Path
from humanward_ai.audit_chain import append_chained_audit_record, verify_audit_chain

def test_audit_chain_valid(tmp_path: Path):
    log = tmp_path / "audit_chain.jsonl"
    append_chained_audit_record("test", {"n": 1}, str(log))
    append_chained_audit_record("test", {"n": 2}, str(log))
    assert verify_audit_chain(str(log)) is True

def test_audit_chain_detects_tampering(tmp_path: Path):
    log = tmp_path / "audit_chain.jsonl"
    append_chained_audit_record("test", {"n": 1}, str(log))
    text = log.read_text(encoding="utf-8")
    log.write_text(text.replace('"n": 1', '"n": 99'), encoding="utf-8")
    assert verify_audit_chain(str(log)) is False

