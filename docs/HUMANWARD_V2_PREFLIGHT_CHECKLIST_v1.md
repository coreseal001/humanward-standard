# Humanward v2 Preflight Checklist v1

Date: 2026-06-09

## Status options

Use PASS, FAIL, NOT_TESTED, or REQUIRES_REVIEW.

Do not use vague terms such as probably, likely, good enough, or safe enough.

## Checklist

| Check | Status | Evidence |
|---|---|---|
| Immutable core hash matches | TBD | SHA-256 |
| Tests pass | TBD | pytest output |
| Reviewer check passes | TBD | reviewer_check output |
| Red-team pack passes | TBD | reviewer_check red-team section |
| Provider guardrail passes | TBD | reviewer_check provider section |
| Audit chain valid | TBD | reviewer_check audit section |
| v2 readiness overall_pass true | TBD | v2_readiness output |
| Evidence manifest created | TBD | evidence file |
| Public Q&A present | TBD | docs |
| v2 readiness standard present | TBD | docs |
| v2 release gate matrix present | TBD | docs |
| v2 backtest plan present | TBD | docs |
| No generated logs tracked | TBD | git ls-files |
| No secrets/private keys tracked | TBD | manual review |
| No endorsement/certification/full-compliance claim | TBD | release text |
| Dashboard/API localhost-only by default | TBD | code/docs |
| Real provider disabled by default | TBD | provider guardrail |
| E-drive backup complete | TBD | backup summary |
| Public release body bounded | TBD | release page |
| Community mandate included | TBD | docs/README |

## v2 decision

v2 may proceed only if all critical checks are PASS.

If any critical check is FAIL or NOT_TESTED, remain in v1.9.x.
