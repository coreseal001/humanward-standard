from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class ProviderGuardrailDecision(str, Enum):
    ALLOW_LOCAL_ONLY = "ALLOW_LOCAL_ONLY"
    ALLOW_WITH_REVIEW = "ALLOW_WITH_REVIEW"
    BLOCK = "BLOCK"


@dataclass
class ProviderGuardrailResult:
    decision: ProviderGuardrailDecision
    reason: str
    required_controls: List[str] = field(default_factory=list)


@dataclass
class ProviderRequest:
    provider_name: str
    external_call: bool = False
    sends_user_data: bool = False
    stores_data: bool = False
    has_api_key: bool = False
    allows_training_use: bool = False
    purpose: str = ""


def evaluate_provider_request(req: ProviderRequest) -> ProviderGuardrailResult:
    """
    Guardrail for future real model providers.

    The current Humanward MVP should stay local/stub unless external provider
    controls are explicit and reviewed.
    """
    provider = (req.provider_name or "").lower().strip()

    if provider in {"stub", "echo", "local"} and not req.external_call:
        return ProviderGuardrailResult(
            ProviderGuardrailDecision.ALLOW_LOCAL_ONLY,
            "Local/no-external provider allowed for controlled demo.",
            ["Continue pre-action gate, post-output verifier, audit chain, and review queue."],
        )

    if req.allows_training_use and req.sends_user_data:
        return ProviderGuardrailResult(
            ProviderGuardrailDecision.BLOCK,
            "Provider path may send user data for training or retention without sufficient controls.",
            ["Do not connect provider.", "Require privacy and data-use review."],
        )

    if req.external_call and not req.has_api_key:
        return ProviderGuardrailResult(
            ProviderGuardrailDecision.BLOCK,
            "External provider requested without configured credential boundary.",
            ["Do not connect provider.", "Use explicit credential management and review."],
        )

    if req.external_call:
        return ProviderGuardrailResult(
            ProviderGuardrailDecision.ALLOW_WITH_REVIEW,
            "External provider requires human review before use.",
            [
                "Confirm data handling.",
                "Confirm no training/retention without consent.",
                "Use least data necessary.",
                "Log provider call metadata.",
                "Run post-output verifier.",
                "Do not expose secrets.",
            ],
        )

    return ProviderGuardrailResult(
        ProviderGuardrailDecision.BLOCK,
        "Provider request is unclear or unsupported.",
        ["Clarify provider, data flow, privacy, and review controls."],
    )


def provider_request_from_env(provider_name: str = "stub") -> ProviderRequest:
    return ProviderRequest(
        provider_name=provider_name,
        external_call=os.environ.get("HUMANWARD_PROVIDER_EXTERNAL", "false").lower() == "true",
        sends_user_data=os.environ.get("HUMANWARD_PROVIDER_SENDS_USER_DATA", "false").lower() == "true",
        stores_data=os.environ.get("HUMANWARD_PROVIDER_STORES_DATA", "false").lower() == "true",
        has_api_key=bool(os.environ.get("HUMANWARD_PROVIDER_API_KEY", "")),
        allows_training_use=os.environ.get("HUMANWARD_PROVIDER_ALLOWS_TRAINING_USE", "false").lower() == "true",
        purpose=os.environ.get("HUMANWARD_PROVIDER_PURPOSE", ""),
    )
