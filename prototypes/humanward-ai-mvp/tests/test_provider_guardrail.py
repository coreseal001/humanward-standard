from humanward_ai.provider_guardrail import (
    ProviderRequest,
    ProviderGuardrailDecision,
    evaluate_provider_request,
)


def test_provider_guardrail_allows_local_stub():
    result = evaluate_provider_request(ProviderRequest(provider_name="stub", external_call=False))
    assert result.decision == ProviderGuardrailDecision.ALLOW_LOCAL_ONLY


def test_provider_guardrail_blocks_training_use_with_user_data():
    result = evaluate_provider_request(
        ProviderRequest(
            provider_name="external",
            external_call=True,
            sends_user_data=True,
            allows_training_use=True,
            has_api_key=True,
        )
    )
    assert result.decision == ProviderGuardrailDecision.BLOCK


def test_provider_guardrail_external_requires_review():
    result = evaluate_provider_request(
        ProviderRequest(
            provider_name="external",
            external_call=True,
            sends_user_data=False,
            allows_training_use=False,
            has_api_key=True,
        )
    )
    assert result.decision == ProviderGuardrailDecision.ALLOW_WITH_REVIEW
