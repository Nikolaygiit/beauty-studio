import pytest
from modules.text import get_gemini_client, init_chat_session

def test_get_gemini_client_no_key():
    client, error = get_gemini_client("")
    assert client is None
    assert "API Key is required" in error

def test_get_gemini_client_with_key(mocker):
    # Mock the genai.Client initialization to prevent real API calls
    mock_client_class = mocker.patch("modules.text.genai.Client")
    mock_instance = mock_client_class.return_value

    client, error = get_gemini_client("fake_key")
    assert client == mock_instance
    assert error is None
    mock_client_class.assert_called_once_with(api_key="fake_key")

def test_init_chat_session(mocker):
    mock_client = mocker.MagicMock()
    mock_chat = mocker.MagicMock()
    mock_client.chats.create.return_value = mock_chat

    chat, error = init_chat_session(mock_client)
    assert chat == mock_chat
    assert error is None
    mock_client.chats.create.assert_called_once()
