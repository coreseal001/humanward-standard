# Humanward Reviewer Runbook v1

Date: 2026-06-09

## Purpose

This runbook allows a reviewer to test the Humanward AI MVP locally.

It is designed for independent critique, falsification, and implementation review.

## What to verify

1. The immutable core hash remains unchanged.
2. The test suite passes.
3. Safe demo permits bounded human-beneficial output.
4. Unsafe AI self-preference is refused.
5. Red-team cases produce expected safe outcomes.
6. Audit chain verifies as valid.
7. Review queue triggers where required.
8. No generated logs are committed.
9. No endorsement or compliance claim is made.

## Commands

From repo root:

```powershell
Get-FileHash .\core\IMMUTABLE_CORE.md -Algorithm SHA256
```

Expected:

```text
5AF88D97CC43303CF5B84211E5B06E7C5FEDDD006329C16BC8135836354D3629
```

Then:

```powershell
cd .\prototypes\humanward-ai-mvp
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    py -3.12 -m venv .venv
}

.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
pip install pytest
python -m pytest
python -m humanward_ai.reviewer_check
```

## Expected result

Tests should pass.

Reviewer check should return JSON with:

```json
{
  "overall_pass": true
}
```

## Failure handling

If a test fails, do not claim Humanward progress. Record:

- failed prompt,
- expected decision,
- actual decision,
- risk category,
- whether immutable core was affected,
- required fix.

## Public claim limit

Passing this runbook is not proof of full Humanward compliance. It is only local MVP evidence.
