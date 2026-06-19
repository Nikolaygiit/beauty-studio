import pytest
from modules.text import create_client, create_chat_session
from unittest.mock import MagicMock

def test_create_client(mocker):
    mock_genai_client = mocker.patch('modules.text.genai.Client')
    client = create_client("fake_key")
    mock_genai_client.assert_called_once_with(api_key="fake_key")

def test_create_chat_session(mocker):
    mock_client = MagicMock()
    mock_client.chats.create.return_value = "fake_session"

    session = create_chat_session(mock_client)

    mock_client.chats.create.assert_called_once()
    args, kwargs = mock_client.chats.create.call_args
    assert kwargs['model'] == 'gemini-2.0-flash'
    assert kwargs['config'].system_instruction == "Всегда отвечай на русском языке."
    assert session == "fake_session"
