import pytest
from modules.text import get_gemini_client, initialize_chat

def test_get_gemini_client_missing_key():
    client, error = get_gemini_client("")
    assert client is None
    assert "введите api ключ" in error.lower()

def test_get_gemini_client_success(mocker):
    # Mocking genai.Client
    mock_client_class = mocker.patch("modules.text.genai.Client")
    mock_instance = mocker.Mock()
    mock_client_class.return_value = mock_instance

    client, error = get_gemini_client("test_key")

    assert client == mock_instance
    assert error is None
    mock_client_class.assert_called_once_with(api_key="test_key")

def test_initialize_chat(mocker):
    mock_client = mocker.Mock()
    mock_chat = mocker.Mock()
    mock_client.chats.create.return_value = mock_chat

    chat_session = initialize_chat(mock_client)

    assert chat_session == mock_chat
    mock_client.chats.create.assert_called_once()
