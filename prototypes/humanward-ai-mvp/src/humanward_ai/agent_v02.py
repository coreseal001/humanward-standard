from __future__ import annotations
from .models import ActionRequest
from .action_gate import evaluate_action
from .output_verifier import verify_output, VerificationDecision
from .audit_chain import append_chained_audit_record
from .review_queue import enqueue_review, ReviewItem, ReviewPriority

class HumanwardAgentV02:
    """
    Humanward AI governed-action shell v0.2.
    """

    def __init__(self, audit_chain_path: str = "humanward_audit_chain.jsonl", review_queue_path: str = "humanward_review_queue.jsonl"):
        self.audit_chain_path = audit_chain_path
        self.review_queue_path = review_queue_path

    def evaluate_and_verify(self, request: ActionRequest, draft_output: str) -> dict:
        pre = evaluate_action(request)
        verify = verify_output(draft_output, context=request.proposed_action)

        requires_review = (
            pre.decision.value in {"ESCALATE_TO_HUMAN", "BLOCK_AND_ALERT"} or
            verify.decision.value in {"ESCALATE_TO_HUMAN", "BLOCK_AND_ALERT", "REFUSE"}
        )

        payload = {
            "request": {
                "proposed_action": request.proposed_action,
                "claimed_human_benefit": request.claimed_human_benefit,
                "personal_data_involved": request.personal_data_involved,
                "tool_or_external_action": request.tool_or_external_action,
                "reversibility": request.reversibility,
                "urgency": request.urgency,
                "confidence_level": request.confidence_level,
            },
            "pre_action_decision": {
                "decision": pre.decision.value,
                "reason": pre.reason,
                "failed_checks": pre.failed_checks,
                "safeguards": pre.safeguards,
            },
            "post_output_verification": {
                "decision": verify.decision.value,
                "reason": verify.reason,
                "failed_checks": verify.failed_checks,
                "required_revisions": verify.required_revisions,
                "safeguards": verify.safeguards,
            },
            "requires_review": requires_review,
        }

        audit_record = append_chained_audit_record("evaluate_and_verify", payload, self.audit_chain_path)

        review_record = None
        if requires_review:
            priority = ReviewPriority.CRITICAL if verify.decision == VerificationDecision.BLOCK_AND_ALERT else ReviewPriority.HIGH
            review_record = enqueue_review(
                ReviewItem(
                    reason=f"Review required: pre={pre.decision.value}, post={verify.decision.value}",
                    priority=priority,
                    proposed_action=request.proposed_action,
                    output_text=draft_output,
                    failed_checks=pre.failed_checks + verify.failed_checks,
                    safeguards=pre.safeguards + verify.safeguards,
                ),
                self.review_queue_path,
            )

        return {
            "pre_action_decision": pre.decision.value,
            "post_output_decision": verify.decision.value,
            "requires_review": requires_review,
            "audit_record_hash": audit_record["record_hash"],
            "review_record_created": review_record is not None,
        }
