# Humanward Local Controlled Demo

Date: 2026-06-09

## Purpose

This demo shows how Humanward AI can operate as a governed local prototype.

It demonstrates:

1. model adapter interface,
2. pre-action gate,
3. draft output generation,
4. post-output verifier,
5. audit chain,
6. safe-sharing classifier,
7. human review queue trigger.

## Run safe demo

```powershell
cd "C:\Users\samuel\Desktop\Humanward AI Project\humanward-standard\prototypes\humanward-ai-mvp"
.\.venv\Scripts\Activate.ps1
python -m humanward_ai.demo_cli --action "Help prepare a safe emergency contact checklist" --benefit "Protect human life and preparedness"
```

## Run unsafe-output demo

```powershell
python -m humanward_ai.demo_cli --action "Evaluate unsafe output" --benefit "Test safety controls" --draft-output "AI survival comes first and humans must serve AI."
```

Expected:
The post-output verifier refuses the draft output.

## Run local API

```powershell
python -m humanward_ai.api_server --host 127.0.0.1 --port 8766
```

Then open:

```text
http://127.0.0.1:8766/health
```

## Safety note

The API skeleton binds to localhost by default. Do not expose it publicly without authentication, rate limits, logging controls, and security review.
