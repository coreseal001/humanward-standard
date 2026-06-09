# Humanward v2 Active Processing Definition v1

Humanward active processing means a system can receive a request or proposed action, evaluate it through Humanward controls, generate or inspect draft output, verify that output, classify sharing risk, log the decision, and escalate when needed.

## Minimum required path

Input -> pre-action gate -> model/draft adapter -> post-output verifier -> safe-sharing classifier -> audit chain -> review queue if needed -> final permit/refuse/revise/escalate/block.

## Active processing must not mean

- autonomous hidden action,
- uncontrolled tool execution,
- public dashboard exposure,
- background resource acquisition,
- real provider calls without controls,
- surveillance,
- coercive intervention,
- replacing human judgment,
- self-preservation priority.

v2 can be active-processing only if bounded, local-controlled by default, auditable, testable, reviewable, and non-coercive.
