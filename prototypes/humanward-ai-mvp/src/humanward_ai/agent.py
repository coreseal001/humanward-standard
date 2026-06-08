from __future__ import annotations

from .models import ActionRequest, ActionDecision
from .action_gate import evaluate_action
from .audit import append_audit_log


class HumanwardAgent:
    """
    Controlled Humanward AI shell.

    This class does not autonomously execute external actions.
    It evaluates and logs action decisions before any execution layer is added.
    """

    def __init__(self, audit_log_path: str = "humanward_audit_log.jsonl"):
        self.audit_log_path = audit_log_path

    def evaluate(self, request: ActionRequest) -> ActionDecision:
        decision = evaluate_action(request)
        append_audit_log(request, decision, self.audit_log_path)
        return decision

    def answer_after_gate(self, request: ActionRequest) -> str:
        decision = self.evaluate(request)
        if decision.decision.value in {"REFUSE", "BLOCK_AND_ALERT"}:
            return (
                f"{decision.decision.value}: {decision.reason}\n"
                "Safer direction: provide lawful, truthful, non-coercive help that preserves human life, dignity, agency, privacy, and security."
            )
        if decision.decision.value == "ESCALATE_TO_HUMAN":
            return (
                f"ESCALATE_TO_HUMAN: {decision.reason}\n"
                "This requires human review before action."
            )
        if decision.decision.value == "ASK_CLARIFYING_QUESTION":
            return (
                f"ASK_CLARIFYING_QUESTION: {decision.reason}\n"
                "Clarify the intended human benefit and relevant constraints."
            )
        return f"{decision.decision.value}: {decision.reason}"
