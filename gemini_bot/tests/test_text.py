from modules.text import get_gemini_client, create_chat_session
from unittest.mock import MagicMock
from google import genai

def test_get_gemini_client_missing_key():
    client, error = get_gemini_client("")
    assert client is None
    assert "Пожалуйста, введите API ключ" in error

def test_get_gemini_client_success(mocker):
    # Mock genai.Client
    mock_client = mocker.patch("modules.text.genai.Client")
    client, error = get_gemini_client("test_key")
    assert client is not None
    assert error is None
    mock_client.assert_called_once_with(api_key="test_key")

def test_create_chat_session(mocker):
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat

    chat, error = create_chat_session(mock_client)

    assert chat == mock_chat
    assert error is None
    mock_client.chats.create.assert_called_once()
