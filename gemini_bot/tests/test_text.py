from modules.text import get_gemini_client, start_chat_session
from google import genai

def test_get_gemini_client_success(mocker):
    mocker.patch("google.genai.Client")
    client, error = get_gemini_client("test_api_key")
    assert client is not None
    assert error is None

def test_get_gemini_client_no_key():
    client, error = get_gemini_client("")
    assert client is None
    assert error == "Пожалуйста, введите API ключ в боковой панели."

def test_get_gemini_client_error(mocker):
    mocker.patch("google.genai.Client", side_effect=Exception("Mocked error"))
    client, error = get_gemini_client("test_key")
    assert client is None
    assert "Ошибка инициализации Gemini" in error

def test_start_chat_session_no_client():
    chat, error = start_chat_session(None)
    assert chat is None
    assert error == "Клиент Gemini не инициализирован."

def test_start_chat_session_success(mocker):
    mock_client = mocker.Mock()
    mock_chat = mocker.Mock()
    mock_client.chats.create.return_value = mock_chat

    chat, error = start_chat_session(mock_client)
    assert chat == mock_chat
    assert error is None

    # Verify config call
    mock_client.chats.create.assert_called_once()
    kwargs = mock_client.chats.create.call_args[1]
    assert kwargs["model"] == "gemini-2.0-flash"
    assert "Всегда отвечай на русском языке" in kwargs["config"].system_instruction
