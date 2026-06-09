# Humanward AI MVP Reliable Q&A v1

Date: 2026-06-09

## What is this prototype?

This is a local controlled Humanward AI MVP.

It demonstrates how a proposed AI action can be checked before execution, how an outgoing draft can be verified before release, how audit records can be chained, and how risky cases can be sent to review.

## Is this a real autonomous AI?

No.

It is a controlled local prototype. It does not autonomously browse, call external services, acquire resources, or act in the background.

## Does it use a real model provider?

No.

Current adapters are local stub and echo adapters.

This is intentional. Real provider connection must wait until strict provider boundaries are complete.

## Why include a model adapter if no real provider is connected?

Because the architecture must separate capability from governance.

The model adapter creates a future interface while preserving the rule that all output must pass through Humanward controls.

## What is reviewer_check?

`python -m humanward_ai.reviewer_check`

It runs:

- red-team pack,
- audit-chain verification,
- provider guardrail checks.

Expected:

`overall_pass: true`

## What should not be committed?

Do not commit:

- `.venv`,
- `__pycache__`,
- `.pytest_cache`,
- `*.egg-info`,
- audit JSONL logs,
- review queue JSONL logs,
- API keys,
- signing secrets,
- private checkpoint files.

## What is the next engineering risk?

The next major risk is connecting a real model provider too early.

Real provider connection must be disabled by default and reviewed before use.
