import pytest
from unittest.mock import MagicMock
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client

def test_generate_image():
    url, err = generate_image("test prompt")
    assert err is None
    assert "https://image.pollinations.ai/prompt/test%20prompt" in url
    assert "seed=" in url

def test_generate_music(mocker):
    # Mock the Gradio client
    mock_client = MagicMock()
    # Assume it returns a tuple where second element is the path
    mock_client.predict.return_value = ("some_info", "/path/to/audio.wav")

    path, err = generate_music(mock_client, "test music")
    assert err is None
    assert path == "/path/to/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="test music",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_video(mocker):
    # Mock the Gradio client
    mock_client = MagicMock()
    # Assume it returns a dict with 'video' key
    mock_client.predict.return_value = {"video": "/path/to/video.mp4"}

    path, err = generate_video(mock_client, "test video")
    assert err is None
    assert path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once_with(
        "test video",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_get_gemini_client_missing_key():
    client, err = get_gemini_client("")
    assert client is None
    assert err == "Не указан API ключ."
