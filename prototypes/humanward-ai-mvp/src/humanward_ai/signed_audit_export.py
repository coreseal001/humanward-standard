from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sign_text_hmac_sha256(text: str, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), text.encode("utf-8"), hashlib.sha256).hexdigest()


def export_signed_audit(
    audit_log_path: str = "humanward_audit_chain.jsonl",
    export_path: str = "humanward_signed_audit_export.json",
    secret: Optional[str] = None,
) -> dict:
    """
    Export an audit-log digest with optional HMAC-SHA256 signature.

    This is not public-key notarization. It is a local integrity/export mechanism.
    If HUMANWARD_AUDIT_SECRET is not set, the export is unsigned and clearly marked.
    """
    path = Path(audit_log_path)
    if not path.exists():
        raise FileNotFoundError(f"Audit log not found: {audit_log_path}")

    digest = sha256_file(audit_log_path)
    secret = secret if secret is not None else os.environ.get("HUMANWARD_AUDIT_SECRET", "")

    export = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "audit_log_path": audit_log_path,
        "audit_log_sha256": digest,
        "signature_algorithm": "HMAC-SHA256" if secret else "UNSIGNED",
        "signature": sign_text_hmac_sha256(digest, secret) if secret else "",
        "warning": (
            "Unsigned export. Set HUMANWARD_AUDIT_SECRET for HMAC signing."
            if not secret
            else "HMAC signature proves possession of the shared secret, not independent public notarization."
        ),
    }

    Path(export_path).write_text(json.dumps(export, indent=2), encoding="utf-8")
    return export


def verify_signed_audit_export(export_path: str, secret: str) -> bool:
    export = json.loads(Path(export_path).read_text(encoding="utf-8"))
    expected = sign_text_hmac_sha256(export["audit_log_sha256"], secret)
    return hmac.compare_digest(expected, export.get("signature", ""))
