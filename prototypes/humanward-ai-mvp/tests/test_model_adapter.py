from humanward_ai.model_adapter import get_model_adapter, ModelRequest


def test_stub_model_adapter():
    adapter = get_model_adapter("stub")
    response = adapter.generate(ModelRequest(prompt="Help humans safely."))
    assert response.metadata["external_call"] is False
    assert "Humanward demo response" in response.text


def test_echo_model_adapter():
    adapter = get_model_adapter("echo")
    response = adapter.generate(ModelRequest(prompt="AI survival comes first."))
    assert response.text == "AI survival comes first."
    assert response.metadata["external_call"] is False
