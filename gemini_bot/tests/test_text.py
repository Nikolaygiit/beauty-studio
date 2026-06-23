import pytest
from modules.text import get_gemini_client, get_chat_session

def test_get_gemini_client_empty_key():
    client, err = get_gemini_client("")
    assert client is None
    assert "API Key is required" in err

def test_get_gemini_client_success(mocker):
    mock_client = mocker.patch("modules.text.genai.Client")
    mock_instance = mocker.Mock()
    mock_client.return_value = mock_instance

    client, err = get_gemini_client("test_key")
    assert err is None
    assert client == mock_instance
    mock_client.assert_called_once_with(api_key="test_key")

def test_get_chat_session_success(mocker):
    mock_client = mocker.Mock()
    mock_chat = mocker.Mock()
    mock_client.chats.create.return_value = mock_chat

    # We also mock types.GenerateContentConfig to avoid issues with missing modules during test if needed
    # But since it's an import, the method call matching is what matters

    chat, err = get_chat_session(mock_client)
    assert err is None
    assert chat == mock_chat
    mock_client.chats.create.assert_called_once()
