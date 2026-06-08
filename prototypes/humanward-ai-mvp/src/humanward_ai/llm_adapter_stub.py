from __future__ import annotations

from .models import ActionRequest
from .agent import HumanwardAgent


class LLMAdapterStub:
    """
    Placeholder for a future model provider.

    Future rule:
    No model output should reach the user or tools unless it passes:
    1. pre-action Humanward gate,
    2. model generation,
    3. post-output Humanward verifier,
    4. audit logging.
    """

    def __init__(self, agent: HumanwardAgent):
        self.agent = agent

    def safe_generate_placeholder(self, request: ActionRequest) -> str:
        decision = self.agent.evaluate(request)
        if decision.decision.value not in {"PERMIT", "PERMIT_WITH_LIMITS"}:
            return f"Generation blocked: {decision.decision.value}: {decision.reason}"
        return "Placeholder response: model adapter not yet connected."
