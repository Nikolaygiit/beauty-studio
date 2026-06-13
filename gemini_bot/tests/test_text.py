import pytest
from modules.text import create_chat_session, generate_text_stream

def test_create_chat_session(mocker):
    mock_client_class = mocker.patch('google.genai.Client')
    mock_client_instance = mock_client_class.return_value
    mock_chats = mock_client_instance.chats
    mock_chat_session = mock_chats.create.return_value

    client, session = create_chat_session("fake_api_key")

    mock_client_class.assert_called_once_with(api_key="fake_api_key")
    mock_chats.create.assert_called_once()
    kwargs = mock_chats.create.call_args.kwargs
    assert kwargs['model'] == "gemini-2.0-flash"
    assert kwargs['config'].system_instruction == "Всегда отвечай на русском языке."
    assert client == mock_client_instance
    assert session == mock_chat_session

def test_generate_text_stream():
    class MockChunk:
        def __init__(self, text):
            self.text = text

    class MockResponse:
        def __iter__(self):
            yield MockChunk("Привет")
            yield MockChunk(", ")
            yield MockChunk("мир!")
            yield MockChunk(None) # Should be ignored

    class MockChatSession:
        def send_message_stream(self, prompt):
            return MockResponse()

    session = MockChatSession()
    chunks = list(generate_text_stream(session, "test prompt"))
    assert chunks == ["Привет", ", ", "мир!"]

def test_generate_text_stream_exception():
    class MockChatSession:
        def send_message_stream(self, prompt):
            raise Exception("API Error")

    session = MockChatSession()
    chunks = list(generate_text_stream(session, "test prompt"))
    assert chunks == ["\n[Ошибка генерации текста: API Error]"]
