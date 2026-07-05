import pytest
from modules.text import get_gemini_client, init_chat_session, stream_text
from google import genai

def test_get_gemini_client_success(mocker):
    # Mocking genai.Client initialization to prevent real API connection
    mock_client_instance = mocker.Mock(spec=genai.Client)
    mocker.patch('google.genai.Client', return_value=mock_client_instance)

    client, error = get_gemini_client("test_api_key")

    assert client is not None
    assert error is None

def test_get_gemini_client_failure(mocker):
    # Mocking to raise an exception
    mocker.patch('google.genai.Client', side_effect=Exception("API Error"))

    client, error = get_gemini_client("test_api_key")

    assert client is None
    assert "Ошибка авторизации Gemini API" in error

def test_init_chat_session(mocker):
    mock_client = mocker.Mock(spec=genai.Client)
    mock_chats = mocker.Mock()
    mock_session = mocker.Mock()
    mock_chats.create.return_value = mock_session
    mock_client.chats = mock_chats

    session = init_chat_session(mock_client)

    assert session is not None
    mock_chats.create.assert_called_once()
    args, kwargs = mock_chats.create.call_args
    assert kwargs['model'] == "gemini-2.0-flash"
    assert "Ты — полезный ИИ-ассистент" in kwargs['config'].system_instruction

def test_stream_text(mocker):
    mock_session = mocker.Mock()

    class MockChunk:
        def __init__(self, text):
            self.text = text

    # Mock stream response
    mock_stream = [MockChunk("Привет, "), MockChunk("мир!")]
    mock_session.send_message_stream.return_value = mock_stream

    chunks = list(stream_text(mock_session, "test prompt"))

    assert chunks == ["Привет, ", "мир!"]
    mock_session.send_message_stream.assert_called_once_with("test prompt")
