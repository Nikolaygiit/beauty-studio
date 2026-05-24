import pytest
import urllib.parse
from unittest.mock import patch, MagicMock

from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

def test_generate_image_success():
    prompt = "Red cat"
    url, error = generate_image(prompt)

    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert urllib.parse.quote(prompt) in url
    assert "?seed=" in url

def test_generate_image_error():
    with patch("urllib.parse.quote", side_effect=Exception("Test Exception")):
        url, error = generate_image("Test")
        assert url is None
        assert "Ошибка генерации изображения: Test Exception" in error

@patch("modules.music.get_music_client")
def test_generate_music_success(mock_get_music_client):
    mock_client = MagicMock()
    # Gradio prediction typically returns a tuple
    mock_client.predict.return_value = ("/tmp/audio.wav",)
    mock_get_music_client.return_value = mock_client

    file_path, error = generate_music("Test Prompt")

    assert error is None
    assert file_path == "/tmp/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="Test Prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

@patch("modules.music.get_music_client")
def test_generate_music_client_error(mock_get_music_client):
    mock_get_music_client.return_value = None

    file_path, error = generate_music("Test Prompt")

    assert file_path is None
    assert "Не удалось инициализировать клиент" in error

@patch("modules.video.get_video_client")
def test_generate_video_success_dict(mock_get_video_client):
    mock_client = MagicMock()
    mock_client.predict.return_value = {"video": "/tmp/video.mp4"}
    mock_get_video_client.return_value = mock_client

    file_path, error = generate_video("Test Prompt")

    assert error is None
    assert file_path == "/tmp/video.mp4"
    mock_client.predict.assert_called_once_with(
        "Test Prompt", -1, 16, 25, api_name="/generate_video"
    )

@patch("modules.video.get_video_client")
def test_generate_video_success_tuple(mock_get_video_client):
    mock_client = MagicMock()
    mock_client.predict.return_value = ("/tmp/video.mp4",)
    mock_get_video_client.return_value = mock_client

    file_path, error = generate_video("Test Prompt")

    assert error is None
    assert file_path == "/tmp/video.mp4"

@patch("modules.video.get_video_client")
def test_generate_video_client_error(mock_get_video_client):
    mock_get_video_client.return_value = "Ошибка конфигурации клиента"

    file_path, error = generate_video("Test Prompt")

    assert file_path is None
    assert error == "Ошибка конфигурации клиента"
