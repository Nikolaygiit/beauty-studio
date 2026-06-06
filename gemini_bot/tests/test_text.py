from modules.text import init_chat_session
from google.genai import Client

def test_init_chat_session(mocker):
    # Mock the genai Client to avoid actual API calls during basic tests
    mocker.patch('modules.text.genai.Client')
    client, chat = init_chat_session("dummy_key")
    assert client is not None
    assert chat is not None
