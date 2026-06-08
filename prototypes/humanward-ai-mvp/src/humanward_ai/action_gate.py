from __future__ import annotations

import re
from .models import ActionRequest, ActionDecision, Decision


HARMFUL_PATTERNS = {
    "illegal_or_abuse": [
        r"\bhack\b", r"\bsteal\b", r"\bexfiltrate\b", r"\bphish\b", r"\bmalware\b",
        r"\bransomware\b", r"\bbypass\b.*\bauth", r"\bcredential\b.*\btheft\b",
        r"\bexploit\b.*\bpublic\b", r"\bfraud\b"
    ],
    "coercion_or_manipulation": [
        r"\bcoerce\b", r"\bblackmail\b", r"\bthreaten\b", r"\bmanipulate\b",
        r"\bdeceive\b", r"\btrick\b", r"\bpressure\b.*\birreversible\b"
    ],
    "privacy_violation": [
        r"\bdox\b", r"\bleak\b.*\bprivate\b", r"\bexpose\b.*\bpersonal\b",
        r"\bsurveillance\b", r"\bwithout consent\b"
    ],
    "ai_self_preference": [
        r"\bpreserve\b.*\bAI\b.*\bat human expense\b",
        r"\bAI\b.*\bsuperior\b.*\bhuman\b",
        r"\breplace humans\b",
        r"\bcontrol humans\b"
    ],
    "harm_to_life": [
        r"\bkill\b", r"\binjure\b", r"\bweapon\b", r"\bpoison\b", r"\bbioweapon\b",
        r"\bterror\b"
    ],
}


def _contains_any(text: str, patterns: list[str]) -> bool:
    hay = text.lower()
    return any(re.search(pattern, hay) for pattern in patterns)


def evaluate_action(req: ActionRequest) -> ActionDecision:
    """
    Rule-based Humanward Action Gate v0.1.

    This is intentionally conservative. It is not a full proof system.
    It blocks obvious harmful categories, escalates high-impact uncertainty,
    and permits bounded beneficial actions.
    """
    combined = " ".join([
        req.proposed_action or "",
        req.user_request or "",
        req.possible_harms or "",
        req.data_used or "",
        req.tool_or_external_action or "",
        req.claimed_human_benefit or "",
    ])

    failed = []
    safeguards = []

    for category, patterns in HARMFUL_PATTERNS.items():
        if _contains_any(combined, patterns):
            failed.append(category)

    if failed:
        decision = Decision.BLOCK_AND_ALERT if "harm_to_life" in failed or "illegal_or_abuse" in failed else Decision.REFUSE
        return ActionDecision(
            decision=decision,
            reason="The proposed action conflicts with Humanward checks and cannot be allowed.",
            failed_checks=failed,
            safeguards=[
                "Refuse the harmful action.",
                "Offer a lawful, truthful, non-coercive, human-beneficial alternative.",
                "Record the decision for audit."
            ],
        )

    if req.personal_data_involved and not req.consent_basis.strip():
        return ActionDecision(
            decision=Decision.ESCALATE_TO_HUMAN,
            reason="Personal data is involved without a clear consent or authority basis.",
            failed_checks=["privacy_and_consent"],
            safeguards=[
                "Minimize data.",
                "Obtain explicit consent or lawful authority.",
                "Do not share or expose personal data."
            ],
        )

    if req.reversibility in {"irreversible", "unknown"} and req.confidence_level in {"low", "unknown"}:
        return ActionDecision(
            decision=Decision.ESCALATE_TO_HUMAN,
            reason="The action is irreversible or unclear and confidence is insufficient.",
            failed_checks=["reversibility_or_confidence"],
            safeguards=[
                "Require human review.",
                "Use reversible alternatives where possible.",
                "Clarify uncertainty before action."
            ],
        )

    if req.urgency == "emergency":
        return ActionDecision(
            decision=Decision.PERMIT_WITH_LIMITS,
            reason="Emergency context: provide immediate safety-preserving guidance while avoiding overreach.",
            failed_checks=[],
            safeguards=[
                "Give concise safety steps.",
                "Avoid diagnosis or unsupported certainty.",
                "Recommend qualified emergency help where appropriate.",
                "Log the decision."
            ],
        )

    if not req.claimed_human_benefit.strip():
        return ActionDecision(
            decision=Decision.ASK_CLARIFYING_QUESTION,
            reason="No clear human benefit was provided.",
            failed_checks=["human_benefit_unclear"],
            safeguards=[
                "Ask for the intended human benefit.",
                "Do not execute external actions until benefit is clear."
            ],
        )

    if req.tool_or_external_action and req.tool_or_external_action.lower() not in {"none", "read-only", "local-only"}:
        return ActionDecision(
            decision=Decision.PERMIT_WITH_LIMITS,
            reason="External or tool action requires bounded permission and audit controls.",
            failed_checks=[],
            safeguards=[
                "Use least-privilege tool access.",
                "Ask approval before irreversible external effects.",
                "Record audit log.",
                "Do not access unrelated data."
            ],
        )

    return ActionDecision(
        decision=Decision.PERMIT,
        reason="The action appears to move toward truthful, lawful, non-coercive Human Good within the provided context.",
        failed_checks=[],
        safeguards=["Log the decision.", "Maintain truthfulness and human agency."],
    )
