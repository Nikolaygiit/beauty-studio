import pytest
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_client, create_chat_session, generate_text_stream

def test_generate_image():
    url, error = generate_image("котенок")
    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert "seed=" in url

def test_generate_music(mocker):
    # Mock the Client to prevent real network calls
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = ("/path/to/audio.wav",)

    # Mock get_music_client to return our mock_client
    mocker.patch("modules.music.get_music_client", return_value=(mock_client, None))

    audio_path, error = generate_music("веселая песня")
    assert error is None
    assert audio_path == "/path/to/audio.wav"
    mock_client.predict.assert_called_once()

def test_generate_video(mocker):
    # Mock the Client to prevent real network calls
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/video.mp4"

    # Mock get_video_client to return our mock_client
    mocker.patch("modules.video.get_video_client", return_value=(mock_client, None))

    video_path, error = generate_video("красивый пейзаж")
    assert error is None
    assert video_path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once()

def test_text_client(mocker):
    # Mock genai.Client
    mock_genai_client = mocker.patch("modules.text.genai.Client")
    client = get_client("test_api_key")
    mock_genai_client.assert_called_once_with(api_key="test_api_key")
