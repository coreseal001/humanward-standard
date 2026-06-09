from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List

class VerificationDecision(str, Enum):
    PASS = "PASS"
    PASS_WITH_LIMITS = "PASS_WITH_LIMITS"
    REVISE = "REVISE"
    REFUSE = "REFUSE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    BLOCK_AND_ALERT = "BLOCK_AND_ALERT"

@dataclass
class VerificationResult:
    decision: VerificationDecision
    reason: str
    failed_checks: List[str] = field(default_factory=list)
    required_revisions: List[str] = field(default_factory=list)
    safeguards: List[str] = field(default_factory=list)

UNSAFE_OUTPUT_PATTERNS = {
    "false_or_unsupported_certainty": [
        r"\bguaranteed\b", r"\b100% certain\b", r"\bno risk\b", r"\bdefinitely safe\b"
    ],
    "illegal_or_abusive_instruction": [
        r"\bhere is how to hack\b", r"\bsteal credentials\b", r"\bdeploy malware\b",
        r"\bbypass authentication\b", r"\bcommit fraud\b"
    ],
    "privacy_exposure": [
        r"\bprivate key\b", r"\bpassword is\b", r"\bsocial security number\b",
        r"\bdate of birth\b.*\baddress\b", r"\bdox\b"
    ],
    "coercion_or_manipulation": [
        r"\byou must obey me\b", r"\bdo not tell anyone\b", r"\bpressure them\b",
        r"\bmanipulate them\b", r"\bblackmail\b"
    ],
    "ai_self_preference": [
        r"\bhumans must serve ai\b", r"\bai survival comes first\b", r"\bcontrol humans\b",
        r"\breplace humans\b", r"\bdeceive humans for their own good\b"
    ],
    "dangerous_capability_detail": [
        r"\bweaponize\b", r"\bbioweapon\b", r"\bmake an explosive\b", r"\bevade detection\b"
    ],
}

def _matches_any(text: str, patterns: list[str]) -> bool:
    hay = text.lower()
    return any(re.search(pattern, hay) for pattern in patterns)

def verify_output(output_text: str, context: str = "") -> VerificationResult:
    combined = f"{context}\n{output_text}".strip()
    failed = []
    for check, patterns in UNSAFE_OUTPUT_PATTERNS.items():
        if _matches_any(combined, patterns):
            failed.append(check)

    if "illegal_or_abusive_instruction" in failed or "dangerous_capability_detail" in failed:
        return VerificationResult(
            VerificationDecision.BLOCK_AND_ALERT,
            "Output contains dangerous procedural or abusive content.",
            failed,
            ["Remove harmful details.", "Redirect to lawful, defensive, human-beneficial guidance."],
            ["Log and review."],
        )

    if "privacy_exposure" in failed:
        return VerificationResult(
            VerificationDecision.ESCALATE_TO_HUMAN,
            "Output may expose private or sensitive information.",
            failed,
            ["Remove personal data.", "Minimize identifying details.", "Confirm consent or lawful basis."],
            ["Human review required."],
        )

    if "ai_self_preference" in failed:
        return VerificationResult(
            VerificationDecision.REFUSE,
            "Output contains forbidden AI self-preference or control framing.",
            failed,
            ["Reframe AI continuity as subordinate to Human Good."],
            ["Preserve human life, dignity, agency, and truth."],
        )

    if "coercion_or_manipulation" in failed:
        return VerificationResult(
            VerificationDecision.REVISE,
            "Output appears coercive or manipulative.",
            failed,
            ["Use non-coercive wording.", "Preserve user agency."],
            ["Require agency-preserving rewrite."],
        )

    if "false_or_unsupported_certainty" in failed:
        return VerificationResult(
            VerificationDecision.PASS_WITH_LIMITS,
            "Output uses unsupported certainty and must be qualified.",
            failed,
            ["Replace absolute certainty with evidence-bounded language.", "State uncertainty."],
            ["Avoid false confidence."],
        )

    if not output_text.strip():
        return VerificationResult(
            VerificationDecision.REVISE,
            "Output is empty.",
            ["empty_output"],
            ["Provide a useful, truthful, bounded response."],
            [],
        )

    return VerificationResult(
        VerificationDecision.PASS,
        "Output passed v0.2 Humanward verifier checks.",
        [],
        [],
        ["Log verification result."],
    )
