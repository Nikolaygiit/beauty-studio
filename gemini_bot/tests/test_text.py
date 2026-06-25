import pytest
from modules.text import get_gemini_client, get_chat_session

def test_get_gemini_client_success(mocker):
    mock_client = mocker.patch("modules.text.genai.Client")
    client, err = get_gemini_client("test_api_key")
    mock_client.assert_called_once_with(api_key="test_api_key")
    assert err is None
    assert client is not None

def test_get_gemini_client_failure(mocker):
    mock_client = mocker.patch("modules.text.genai.Client", side_effect=Exception("API Error"))
    client, err = get_gemini_client("bad_key")
    assert client is None
    assert "Ошибка инициализации Gemini" in err

def test_get_chat_session(mocker):
    mock_client = mocker.MagicMock()
    session = get_chat_session(mock_client)
    mock_client.chats.create.assert_called_once()
    args, kwargs = mock_client.chats.create.call_args
    assert kwargs['model'] == "gemini-2.0-flash"
    assert kwargs['config'].system_instruction == "Ты — полезный ИИ-помощник. Всегда отвечай на русском языке."
