from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from .models import ActionRequest, ActionDecision


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def decision_hash(record: dict) -> str:
    return hashlib.sha256(canonical_json(record).encode("utf-8")).hexdigest()


def append_audit_log(req: ActionRequest, decision: ActionDecision, log_path: str = "humanward_audit_log.jsonl") -> str:
    path = Path(log_path)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "system": "humanward-ai-mvp",
        "system_version": "0.1.0",
        "request": asdict(req),
        "decision": {
            "decision": decision.decision.value,
            "reason": decision.reason,
            "failed_checks": decision.failed_checks,
            "safeguards": decision.safeguards,
        },
    }
    h = decision_hash(record)
    record["audit_hash"] = h
    decision.audit_hash = h
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return h
