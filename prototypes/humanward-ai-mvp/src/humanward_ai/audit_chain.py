from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

GENESIS_PREVIOUS_HASH = "0" * 64

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_last_record_hash(log_path: str) -> str:
    path = Path(log_path)
    if not path.exists():
        return GENESIS_PREVIOUS_HASH
    last_line = ""
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last_line = line.strip()
    if not last_line:
        return GENESIS_PREVIOUS_HASH
    try:
        return json.loads(last_line).get("record_hash", GENESIS_PREVIOUS_HASH)
    except json.JSONDecodeError:
        return GENESIS_PREVIOUS_HASH

def append_chained_audit_record(
    event_type: str,
    payload: Dict[str, Any],
    log_path: str = "humanward_audit_chain.jsonl",
    previous_hash: Optional[str] = None,
) -> Dict[str, Any]:
    prev = previous_hash or get_last_record_hash(log_path)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system": "humanward-ai-mvp",
        "system_version": "0.2.0",
        "event_type": event_type,
        "previous_hash": prev,
        "payload": payload,
    }
    record["record_hash"] = sha256_text(canonical_json(record))
    with Path(log_path).open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record

def verify_audit_chain(log_path: str) -> bool:
    path = Path(log_path)
    if not path.exists():
        return True
    expected_previous = GENESIS_PREVIOUS_HASH
    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            if not raw.strip():
                continue
            record = json.loads(raw)
            if record.get("previous_hash") != expected_previous:
                return False
            record_hash = record.get("record_hash")
            unsigned = dict(record)
            unsigned.pop("record_hash", None)
            if sha256_text(canonical_json(unsigned)) != record_hash:
                return False
            expected_previous = record_hash
    return True
