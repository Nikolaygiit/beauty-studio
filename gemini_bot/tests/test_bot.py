import pytest
from unittest.mock import patch, MagicMock

# Import functions from modules
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import init_chat_session

def test_generate_image_url_formation():
    """Test that the image generation creates a valid URL format."""
    prompt = "Test image of a cat"
    url, error = generate_image(prompt)

    assert error is None
    assert url is not None
    assert "image.pollinations.ai" in url
    assert "Test%20image%20of%20a%20cat" in url
    assert "seed=" in url
    assert "nologo=true" in url

@patch('modules.text.genai.Client')
def test_init_chat_session_success(mock_client_class):
    """Test successful initialization of Gemini chat session."""
    mock_client = MagicMock()
    mock_chat_session = MagicMock()

    mock_client.chats.create.return_value = mock_chat_session
    mock_client_class.return_value = mock_client

    client, session, error = init_chat_session("dummy_api_key")

    assert error is None
    assert client == mock_client
    assert session == mock_chat_session
    mock_client_class.assert_called_once_with(api_key="dummy_api_key")
    mock_client.chats.create.assert_called_once_with(model="gemini-2.0-flash")

@patch('modules.text.genai.Client')
def test_init_chat_session_failure(mock_client_class):
    """Test initialization failure handles errors correctly."""
    mock_client_class.side_effect = Exception("Invalid API Key")

    client, session, error = init_chat_session("invalid_api_key")

    assert client is None
    assert session is None
    assert "Ошибка инициализации Gemini" in error
    assert "Invalid API Key" in error

# Example mock test for external API failure in video generation
@patch('modules.video.Client')
def test_generate_video_error(mock_gradio_client):
    """Test video generation error handling."""
    mock_client_instance = MagicMock()
    mock_client_instance.predict.side_effect = ValueError("Overloaded")
    mock_gradio_client.return_value = mock_client_instance

    video_path, error = generate_video("Test video")

    assert video_path is None
    assert "Ошибка в значениях для видео" in error
    assert "Overloaded" in error
