import pytest
from unittest.mock import patch, MagicMock

from gemini_bot.modules.text import init_gemini_client, init_chat_session
from gemini_bot.modules.image import generate_image
from gemini_bot.modules.music import generate_music
from gemini_bot.modules.video import generate_video

# Tests for Text Module
def test_init_gemini_client_missing_key():
    client, err = init_gemini_client(None)
    assert client is None
    assert err == "API Key is missing."

@patch('gemini_bot.modules.text.genai.Client')
def test_init_gemini_client_success(mock_client_class):
    mock_instance = MagicMock()
    mock_client_class.return_value = mock_instance
    client, err = init_gemini_client("test_key")
    assert err is None
    assert client == mock_instance

def test_init_chat_session_missing_client():
    chat, err = init_chat_session(None)
    assert chat is None
    assert err == "Gemini client is not initialized."

# Tests for Image Module
def test_generate_image_missing_prompt():
    url, err = generate_image(None)
    assert url is None
    assert err == "Prompt is missing."

def test_generate_image_success():
    url, err = generate_image("test prompt")
    assert err is None
    assert url.startswith("https://image.pollinations.ai/prompt/test%20prompt?seed=")

# Tests for Music Module
def test_generate_music_missing_prompt():
    music, err = generate_music(None)
    assert music is None
    assert err == "Prompt is missing."

@patch('gemini_bot.modules.music.Client')
def test_generate_music_success(mock_client_class):
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = "fake_audio_path.wav"
    mock_client_class.return_value = mock_client_instance

    music, err = generate_music("happy song")
    assert err is None
    assert music == "fake_audio_path.wav"
    mock_client_instance.predict.assert_called_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

# Tests for Video Module
def test_generate_video_missing_prompt():
    video, err = generate_video(None)
    assert video is None
    assert err == "Prompt is missing."

@patch('gemini_bot.modules.video.Client')
def test_generate_video_success_string(mock_client_class):
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = "fake_video_path.mp4"
    mock_client_class.return_value = mock_client_instance

    video, err = generate_video("a cat playing")
    assert err is None
    assert video == "fake_video_path.mp4"
    mock_client_instance.predict.assert_called_with(
        "a cat playing",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

@patch('gemini_bot.modules.video.Client')
def test_generate_video_success_dict(mock_client_class):
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = {'video': 'fake_video_path_from_dict.mp4'}
    mock_client_class.return_value = mock_client_instance

    video, err = generate_video("a cat playing")
    assert err is None
    assert video == "fake_video_path_from_dict.mp4"
