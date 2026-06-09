# Humanward Signed Audit Export v1

Date: 2026-06-09

## Purpose

Humanward needs audit evidence that can be exported and checked.

The current MVP supports hash-chained audit logs and HMAC-SHA256 export digests.

## Current capability

The signed audit export:

- calculates SHA-256 of the audit chain file,
- optionally signs the digest with HMAC-SHA256,
- writes an export JSON file,
- supports verification when the same secret is provided.

## Important limitation

HMAC is not public notarization. It proves possession of a shared secret. It does not prove independent timestamping or public immutability.

Future improvement should add:

- public-key signatures,
- OpenTimestamps or equivalent timestamp proof,
- append-only remote storage,
- release-linked audit manifests.

## Recommended command

```powershell
$env:HUMANWARD_AUDIT_SECRET = "replace-with-local-secret"
python - <<'PY'
from humanward_ai.signed_audit_export import export_signed_audit
print(export_signed_audit("humanward_audit_chain.jsonl", "humanward_signed_audit_export.json"))
PY
```

Do not commit generated audit files.
