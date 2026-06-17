import pytest
from modules.text import get_gemini_client

def test_get_gemini_client_no_key():
    client, err = get_gemini_client("")
    assert client is None
    assert "API key is required" in err

def test_get_gemini_client_success(mocker):
    mock_genai_client = mocker.MagicMock()
    mock_chat = mocker.MagicMock()

    # Correctly mock the client initialization
    mocker.patch("modules.text.genai.Client", return_value=mock_genai_client)
    mock_genai_client.chats.create.return_value = mock_chat

    client, chat = get_gemini_client("fake_api_key")

    assert client == mock_genai_client
    assert chat == mock_chat
