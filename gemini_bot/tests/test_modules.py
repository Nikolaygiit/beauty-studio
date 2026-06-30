import pytest
from unittest.mock import MagicMock
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client, initialize_chat_session

def test_generate_image():
    url, err = generate_image("test prompt")
    assert url is not None
    assert err is None
    assert "image.pollinations.ai" in url
    assert "test%20prompt" in url

def test_generate_image_empty():
    url, err = generate_image("")
    assert url is None
    assert err == "Prompt is required to generate an image."

def test_generate_music(mocker):
    # Mock get_music_client
    mock_client = MagicMock()
    mock_client.predict.return_value = "path/to/audio.wav"
    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    path, err = generate_music("test music prompt")
    assert path == "path/to/audio.wav"
    assert err is None
    mock_client.predict.assert_called_once()

def test_generate_video(mocker):
    # Mock get_video_client
    mock_client = MagicMock()
    mock_client.predict.return_value = "path/to/video.mp4"
    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    path, err = generate_video("test video prompt")
    assert path == "path/to/video.mp4"
    assert err is None
    mock_client.predict.assert_called_once()

def test_get_gemini_client(mocker):
    # Mock genai.Client
    mock_genai = mocker.patch('modules.text.genai')
    mock_client_instance = MagicMock()
    mock_genai.Client.return_value = mock_client_instance

    client, err = get_gemini_client("fake_key")
    assert client == mock_client_instance
    assert err is None

    # Test error
    mock_genai.Client.side_effect = Exception("Test Error")
    client, err = get_gemini_client("fake_key")
    assert client is None
    assert "Test Error" in err

def test_initialize_chat_session():
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat

    chat = initialize_chat_session(mock_client)
    assert chat == mock_chat

    # Test error
    mock_client.chats.create.side_effect = Exception("Test Error")
    chat = initialize_chat_session(mock_client)
    assert chat is None
