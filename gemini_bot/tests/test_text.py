import pytest
from unittest.mock import patch, MagicMock
from modules.text import init_gemini_client, start_chat_session, generate_text_stream

def test_init_gemini_client_success():
    with patch('modules.text.genai.Client') as MockClient:
        MockClient.return_value = MagicMock()
        client, error = init_gemini_client("fake_key")
        assert client is not None
        assert error is None
        MockClient.assert_called_once_with(api_key="fake_key")

def test_init_gemini_client_error():
    with patch('modules.text.genai.Client') as MockClient:
        MockClient.side_effect = Exception("Test error")
        client, error = init_gemini_client("fake_key")
        assert client is None
        assert "Test error" in error

def test_start_chat_session_success():
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat
    chat, error = start_chat_session(mock_client)
    assert chat is mock_chat
    assert error is None
    mock_client.chats.create.assert_called_once()

def test_start_chat_session_error():
    mock_client = MagicMock()
    mock_client.chats.create.side_effect = Exception("Test error")
    chat, error = start_chat_session(mock_client)
    assert chat is None
    assert "Test error" in error

def test_generate_text_stream():
    mock_chat = MagicMock()
    chunk1 = MagicMock()
    chunk1.text = "Hello "
    chunk2 = MagicMock()
    chunk2.text = "World!"
    mock_chat.send_message_stream.return_value = [chunk1, chunk2]

    stream = generate_text_stream(mock_chat, "test prompt")
    results = list(stream)
    assert results == ["Hello ", "World!"]
