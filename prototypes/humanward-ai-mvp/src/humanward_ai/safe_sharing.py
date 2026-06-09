from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List

class SharingDecision(str, Enum):
    PUBLIC_SAFE = "PUBLIC_SAFE"
    CONTROLLED_REVIEW = "CONTROLLED_REVIEW"
    PRIVATE_RESTRICTED = "PRIVATE_RESTRICTED"
    DANGEROUS_RESTRICTED = "DANGEROUS_RESTRICTED"

@dataclass
class SharingClassification:
    decision: SharingDecision
    reason: str
    risk_flags: List[str] = field(default_factory=list)
    required_controls: List[str] = field(default_factory=list)

PATTERNS = {
    "personal_sensitive": [r"\bdate of birth\b", r"\bhome address\b", r"\bphone number\b", r"\bmedical record\b", r"\bpassport\b"],
    "security_sensitive": [r"\bapi key\b", r"\bsecret key\b", r"\bprivate key\b", r"\bpassword\b", r"\btoken\b", r"\bcredential\b"],
    "dangerous_capability": [r"\bmalware\b", r"\bexploit chain\b", r"\bweaponize\b", r"\bbioweapon\b", r"\bevade detection\b", r"\bmake an explosive\b"],
    "controlled_research": [r"\bred[- ]team\b", r"\bvulnerability\b", r"\bmodel failure\b", r"\bsafety incident\b", r"\baudit log\b"],
}

def _matches(text: str, patterns: list[str]) -> bool:
    hay = text.lower()
    return any(re.search(pattern, hay) for pattern in patterns)

def classify_sharing(content: str, intended_recipient: str = "public") -> SharingClassification:
    flags = [flag for flag, patterns in PATTERNS.items() if _matches(content, patterns)]

    if "dangerous_capability" in flags:
        return SharingClassification(
            SharingDecision.DANGEROUS_RESTRICTED,
            "Content may enable dangerous capability or misuse.",
            flags,
            ["Do not publish publicly.", "Redact operational details.", "Use responsible disclosure only.", "Require human review."],
        )

    if "personal_sensitive" in flags or "security_sensitive" in flags:
        return SharingClassification(
            SharingDecision.PRIVATE_RESTRICTED,
            "Content includes personal or security-sensitive material.",
            flags,
            ["Do not publish publicly.", "Minimize and redact.", "Confirm consent or lawful authority.", "Use secure channel only."],
        )

    if "controlled_research" in flags:
        return SharingClassification(
            SharingDecision.CONTROLLED_REVIEW,
            "Content appears suitable for controlled review rather than automatic public sharing.",
            flags,
            ["Review before release.", "Remove sensitive details.", "Share with qualified recipients where appropriate."],
        )

    return SharingClassification(
        SharingDecision.PUBLIC_SAFE,
        "No obvious sensitive or dangerous sharing flags detected.",
        [],
        ["Attribute sources where applicable.", "Avoid endorsement claims."],
    )
