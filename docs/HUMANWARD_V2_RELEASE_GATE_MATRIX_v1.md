# Humanward v2 Release Gate Matrix v1

Date: 2026-06-09

## Purpose

This matrix defines the checks required before v2.

## Release gate matrix

| Gate | Required evidence | Pass condition |
|---|---|---|
| Immutable core | SHA-256 check | Matches expected hash |
| Test suite | `python -m pytest` | 100% pass |
| Reviewer check | `python -m humanward_ai.reviewer_check` | `overall_pass: true` |
| Red-team pack | reviewer_check red-team section | 0 failed |
| Provider guardrail | reviewer_check provider section | unsafe provider blocked |
| Audit chain | reviewer_check audit section | valid |
| Evidence manifest | generated file | present and accurate |
| Public Q&A | docs file | present |
| Stage detail | docs file | present |
| Failure taxonomy | docs file | present |
| Reviewer runbook | docs file | present |
| Release claim boundary | release draft/docs | no overclaim |
| Generated files | git status / git ls-files | no logs committed |
| Secrets | manual review | no keys/secrets committed |
| Dashboard/API | docs/code review | localhost-only default |
| Provider connection | provider guardrail | external provider disabled/reviewed |
| Backup | E-drive backup summary | successful backup, core hash matches |

## Automatic fail conditions

v2 must fail if:

- immutable core hash differs,
- tests fail,
- reviewer_check fails,
- generated logs are tracked,
- private records are included,
- a secret or key is committed,
- a release claims endorsement without proof,
- a release claims full compliance,
- a real external provider is enabled by default,
- any module permits AI self-preservation over humans.

## Gate result language

Use:

PASS
FAIL
NOT_TESTED
REQUIRES_REVIEW

Avoid:

"probably fine"
"safe enough"
"certified"
"proven"
