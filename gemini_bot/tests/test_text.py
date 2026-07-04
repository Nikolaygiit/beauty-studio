import pytest
from modules.text import get_gemini_client, get_chat_session, generate_text_stream

def test_get_gemini_client_success(mocker):
    # Mock genai.Client
    mock_client_class = mocker.patch("modules.text.genai.Client")
    mock_client_instance = mocker.MagicMock()
    mock_client_class.return_value = mock_client_instance

    client, error = get_gemini_client("fake_key")

    assert error is None
    assert client == mock_client_instance
    mock_client_class.assert_called_once_with(api_key="fake_key")

def test_get_gemini_client_empty_key():
    client, error = get_gemini_client("")
    assert client is None
    assert "Пожалуйста, введите API ключ" in error

def test_get_chat_session_success(mocker):
    mock_client = mocker.MagicMock()
    mock_chat = mocker.MagicMock()
    mock_client.chats.create.return_value = mock_chat

    # We mock genai.types.GenerateContentConfig just to prevent import errors if not strictly necessary,
    # but the mocked client should handle it.

    chat, error = get_chat_session(mock_client)

    assert error is None
    assert chat == mock_chat
    mock_client.chats.create.assert_called_once()
