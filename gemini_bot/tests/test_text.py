from modules.text import get_gemini_client, init_chat_session, generate_text_stream

def test_get_gemini_client_success(mocker):
    mock_genai = mocker.patch('modules.text.genai.Client')
    mock_genai.return_value = "mock_client"

    client = get_gemini_client("fake_api_key")
    assert client == "mock_client"
    mock_genai.assert_called_once_with(api_key="fake_api_key")

def test_init_chat_session(mocker):
    mock_client = mocker.MagicMock()
    mock_client.chats.create.return_value = "mock_session"

    session = init_chat_session(mock_client)
    assert session == "mock_session"
    mock_client.chats.create.assert_called_once()

def test_generate_text_stream(mocker):
    mock_session = mocker.MagicMock()

    # Mocking response chunks
    class MockChunk:
        def __init__(self, text):
            self.text = text

    mock_session.send_message_stream.return_value = [
        MockChunk("Привет"), MockChunk(", "), MockChunk("мир!")
    ]

    chunks = list(generate_text_stream(mock_session, "Скажи привет"))

    assert chunks == ["Привет", ", ", "мир!"]
    mock_session.send_message_stream.assert_called_once_with("Скажи привет")
