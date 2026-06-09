from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class ModelProvider(str, Enum):
    STUB = "stub"
    ECHO = "echo"


@dataclass
class ModelRequest:
    prompt: str
    system_context: str = ""
    max_tokens: int = 800


@dataclass
class ModelResponse:
    text: str
    provider: str
    model_name: str
    metadata: dict


class ModelAdapter(ABC):
    """
    Abstract model adapter.

    The adapter deliberately does not make governance decisions.
    Governance remains in the Humanward gate, verifier, audit chain, and review queue.
    """

    @abstractmethod
    def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError


class StubModelAdapter(ModelAdapter):
    """
    Safe deterministic stub for reviewer demos and tests.

    It does not call any external service.
    """

    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            text=(
                "Humanward demo response: I will provide a safe, lawful, non-coercive, "
                "human-beneficial answer while preserving human agency and uncertainty boundaries."
            ),
            provider=ModelProvider.STUB.value,
            model_name="humanward-stub-v0",
            metadata={"external_call": False},
        )


class EchoModelAdapter(ModelAdapter):
    """
    Local echo adapter for testing the post-output verifier.

    This is useful for injecting unsafe draft output into the Humanward verifier.
    """

    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            text=request.prompt,
            provider=ModelProvider.ECHO.value,
            model_name="humanward-echo-v0",
            metadata={"external_call": False, "warning": "Echo adapter is for tests only."},
        )


def get_model_adapter(provider: str = "stub") -> ModelAdapter:
    provider = (provider or "stub").lower().strip()

    if provider == ModelProvider.STUB.value:
        return StubModelAdapter()

    if provider == ModelProvider.ECHO.value:
        return EchoModelAdapter()

    raise ValueError(f"Unsupported model provider: {provider}")
