import pytest
from modules.text import get_gemini_client, get_chat_session, generate_text_stream

def test_get_gemini_client_missing_key():
    client, error = get_gemini_client("")
    assert client is None
    assert "API key is required" in error

def test_get_gemini_client_success(mocker):
    mocker.patch('modules.text.genai.Client', return_value="mocked_client")
    client, error = get_gemini_client("test_key")
    assert client == "mocked_client"
    assert error is None

def test_generate_text_stream(mocker):
    mock_chunk = mocker.MagicMock()
    mock_chunk.text = "chunk_text"

    mock_response = [mock_chunk]

    mock_chat_session = mocker.MagicMock()
    mock_chat_session.send_message_stream.return_value = mock_response

    stream = generate_text_stream(mock_chat_session, "test prompt")
    result = list(stream)

    assert result == ["chunk_text"]
    mock_chat_session.send_message_stream.assert_called_once_with("test prompt")
