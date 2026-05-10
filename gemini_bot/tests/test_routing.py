import pytest
from unittest.mock import patch, MagicMock

# The easiest way to test without pulling in streamlit UI state
# is to test the underlying modules that app.py routes to.

def test_image_generation_url_format():
    from modules.image import generate_image
    url, error = generate_image("test prompt")
    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/test%20prompt?seed=")

def test_text_module_get_client():
    from modules.text import get_client
    with patch('modules.text.genai.Client') as mock_client:
        get_client("test_key")
        mock_client.assert_called_once_with(api_key="test_key")

def test_text_module_init_chat_session():
    from modules.text import init_chat_session
    mock_client = MagicMock()
    init_chat_session(mock_client)
    mock_client.chats.create.assert_called_once_with(model="gemini-2.0-flash")

# A simple test to show pytest works
def test_dummy():
    assert True
