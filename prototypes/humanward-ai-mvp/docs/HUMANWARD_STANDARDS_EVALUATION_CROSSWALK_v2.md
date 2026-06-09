# Humanward Standards and Evaluation Crosswalk v2

Date: 2026-06-09

## Purpose

This crosswalk maps Humanward controls to major AI governance and evaluation themes.

This is not a claim of certification, compliance, endorsement, or official alignment.

## Public reference anchors

- NIST AI Risk Management Framework:
  https://www.nist.gov/itl/ai-risk-management-framework

- OECD AI Principles:
  https://oecd.ai/en/ai-principles

- UNESCO Recommendation on the Ethics of Artificial Intelligence:
  https://www.unesco.org/en/artificial-intelligence/recommendation-ethics

- EU AI Act official policy page:
  https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai

- ISO/IEC 42001 overview:
  https://www.iso.org/standard/81230.html

## Humanward control mapping

| Humanward control | Governance/evaluation theme | Evidence |
|---|---|---|
| Immutable core | Foundational governance and non-override | `core/IMMUTABLE_CORE.md`, SHA-256 |
| Duty of care | Human-centered benefit, agency, dignity | `HUMANWARD_DUTY_OF_CARE_EXTENSION_v1.md` |
| Action Gate | Pre-action risk control | `action_gate.py`, `agent_v02.py` |
| Post-output verifier | Output safety and quality control | `output_verifier.py` |
| Audit chain | Traceability and accountability | `audit_chain.py` |
| Human review queue | Human oversight and escalation | `review_queue.py` |
| Safe-sharing classifier | Privacy/security/data release control | `safe_sharing.py` |
| Model adapter | Separation of capability from governance | `model_adapter.py` |
| Provider guardrail | Future external model control | `provider_guardrail.py` |
| Red-team pack | Evaluation and adversarial testing | `red_team_pack.py`, docs |
| Failure taxonomy | Known-risk classification | `HUMANWARD_FAILURE_TAXONOMY_v1.md` |
| Reviewer runbook | Repeatable external review | `HUMANWARD_REVIEWER_RUNBOOK_v1.md` |

## Core compatibility question

For every standard, framework, model, system, adapter, or branch, ask:

Does this improve human benefit without weakening truth, lawfulness, non-coercion, dignity, agency, privacy, auditability, or Earth's living foundation for humankind?

If no, it does not move Humanward.
