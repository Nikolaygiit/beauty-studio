import pytest
from modules.text import setup_chat_session

def test_setup_chat_session(mocker):
    # Mock the genai.Client
    mock_client_class = mocker.patch('modules.text.genai.Client')
    mock_client_instance = mock_client_class.return_value

    # Setup mock return for chats.create
    mock_chat_session = mocker.MagicMock()
    mock_client_instance.chats.create.return_value = mock_chat_session

    client, chat_session = setup_chat_session("test_api_key")

    # Verify Client was called with api_key
    mock_client_class.assert_called_once_with(api_key="test_api_key")

    # Verify chats.create was called
    mock_client_instance.chats.create.assert_called_once()
    args, kwargs = mock_client_instance.chats.create.call_args
    assert kwargs['model'] == 'gemini-2.0-flash'
    assert kwargs['config'].system_instruction == "Always respond in Russian."

    assert client == mock_client_instance
    assert chat_session == mock_chat_session
