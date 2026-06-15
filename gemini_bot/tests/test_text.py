import pytest
from unittest.mock import MagicMock
from modules.text import get_gemini_client, create_chat_session, generate_text_stream

def test_get_gemini_client(mocker):
    mock_genai_client = mocker.patch("modules.text.genai.Client")
    client = get_gemini_client("test_api_key")
    mock_genai_client.assert_called_once_with(api_key="test_api_key")

def test_create_chat_session():
    mock_client = MagicMock()
    session = create_chat_session(mock_client)
    mock_client.chats.create.assert_called_once()

    # Check arguments
    call_kwargs = mock_client.chats.create.call_args.kwargs
    assert call_kwargs["model"] == "gemini-2.0-flash"
    assert "Всегда отвечай на русском языке." in call_kwargs["config"].system_instruction

def test_generate_text_stream():
    mock_session = MagicMock()

    # Mock stream response
    chunk1 = MagicMock()
    chunk1.text = "Hello "
    chunk2 = MagicMock()
    chunk2.text = "world"
    mock_session.send_message_stream.return_value = [chunk1, chunk2]

    stream = generate_text_stream(mock_session, "Say hello")

    results = list(stream)
    assert len(results) == 2
    assert results[0] == ("Hello ", None)
    assert results[1] == ("world", None)

def test_generate_text_stream_error():
    mock_session = MagicMock()
    mock_session.send_message_stream.side_effect = Exception("API error")

    stream = generate_text_stream(mock_session, "Say hello")

    results = list(stream)
    assert len(results) == 1
    assert results[0][0] is None
    assert "Ошибка при генерации текста: API error" in results[0][1]
