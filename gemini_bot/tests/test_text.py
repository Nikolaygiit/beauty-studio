import pytest
from unittest.mock import MagicMock, patch
from modules.text import init_gemini_client, init_chat_session, stream_gemini_response

def test_init_gemini_client():
    client, error = init_gemini_client("test_key")
    assert client is not None
    assert error is None

@patch('modules.text.genai.Client')
def test_init_chat_session(mock_client_class):
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat

    chat, error = init_chat_session(mock_client)
    assert chat == mock_chat
    assert error is None

def test_stream_gemini_response():
    mock_chat_session = MagicMock()
    mock_chunk1 = MagicMock()
    mock_chunk1.text = "Hello"
    mock_chunk2 = MagicMock()
    mock_chunk2.text = " World"

    mock_chat_session.send_message_stream.return_value = [mock_chunk1, mock_chunk2]

    result = list(stream_gemini_response(mock_chat_session, "test prompt"))
    assert result == ["Hello", " World"]
