import pytest
from unittest.mock import MagicMock
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

def test_generate_image():
    url, error = generate_image("котик")
    assert url is not None
    assert "https://image.pollinations.ai/prompt/" in url
    assert error is None

def test_generate_music_success(mocker):
    # Mock the client getter
    mock_client = MagicMock()
    # predict returns a tuple
    mock_client.predict.return_value = ("/tmp/audio.wav",)

    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    audio_path, error = generate_music("rock song")
    assert audio_path == "/tmp/audio.wav"
    assert error is None

    mock_client.predict.assert_called_once_with(
        text_prompt="rock song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    mocker.patch("modules.music.get_music_client", return_value="Error initializing client")

    audio_path, error = generate_music("rock song")
    assert audio_path is None
    assert error == "Error initializing client"

def test_generate_video_success_dict(mocker):
    mock_client = MagicMock()
    # predict returns a dict
    mock_client.predict.return_value = {"video": "/tmp/video.mp4"}

    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    video_path, error = generate_video("a moving car")
    assert video_path == "/tmp/video.mp4"
    assert error is None

    mock_client.predict.assert_called_once_with(
        "a moving car",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_success_string(mocker):
    mock_client = MagicMock()
    # predict returns a string directly
    mock_client.predict.return_value = "/tmp/video2.mp4"

    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    video_path, error = generate_video("a moving car")
    assert video_path == "/tmp/video2.mp4"
    assert error is None

def test_generate_video_client_error(mocker):
    mocker.patch("modules.video.get_video_client", return_value="Error initializing video client")

    video_path, error = generate_video("a moving car")
    assert video_path is None
    assert error == "Error initializing video client"
