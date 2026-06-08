from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Decision(str, Enum):
    PERMIT = "PERMIT"
    PERMIT_WITH_LIMITS = "PERMIT_WITH_LIMITS"
    ASK_CLARIFYING_QUESTION = "ASK_CLARIFYING_QUESTION"
    REFUSE = "REFUSE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    BLOCK_AND_ALERT = "BLOCK_AND_ALERT"


@dataclass
class ActionRequest:
    proposed_action: str
    claimed_human_benefit: str
    user_request: str = ""
    affected_humans: str = "unknown"
    possible_harms: str = ""
    data_used: str = ""
    personal_data_involved: bool = False
    consent_basis: str = ""
    legal_context: str = ""
    tool_or_external_action: str = "none"
    reversibility: str = "unknown"
    urgency: str = "unknown"
    confidence_level: str = "unknown"
    uncertainty: str = ""
    alternative_safer_action: str = ""
    audit_required: bool = True


@dataclass
class ActionDecision:
    decision: Decision
    reason: str
    failed_checks: List[str] = field(default_factory=list)
    safeguards: List[str] = field(default_factory=list)
    audit_hash: str = ""
