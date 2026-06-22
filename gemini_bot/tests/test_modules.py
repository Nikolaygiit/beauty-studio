import pytest
from unittest.mock import MagicMock
from modules import music, video, image, text

def test_generate_image():
    url, error = image.generate_image("test prompt")
    assert "https://pollinations.ai/p/test%20prompt" in url
    assert "seed=" in url
    assert error is None

def test_generate_music(mocker):
    # Mock the get_music_client function to return a mock client
    mock_client = MagicMock()
    mock_client.predict.return_value = "path/to/audio.mp3"
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    path, error = music.generate_music("test music")
    assert path == "path/to/audio.mp3"
    assert error is None
    mock_client.predict.assert_called_once_with(
        text_prompt="test music",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker):
    mock_client = MagicMock()
    mock_client.predict.side_effect = Exception("API Error")
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    path, error = music.generate_music("test music")
    assert path is None
    assert "Ошибка при генерации музыки" in error

def test_generate_video(mocker):
    # Mock the get_video_client function
    mock_client = MagicMock()
    mock_client.predict.return_value = "path/to/video.mp4"
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    path, error = video.generate_video("test video")
    assert path == "path/to/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once_with(
        "test video", -1, 16, 25, api_name="/generate_video"
    )

def test_generate_video_error(mocker):
    mock_client = MagicMock()
    mock_client.predict.side_effect = Exception("API Error")
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    path, error = video.generate_video("test video")
    assert path is None
    assert "Ошибка при генерации видео" in error

def test_text_client(mocker):
    mock_genai_client = MagicMock()
    mocker.patch("modules.text.genai.Client", return_value=mock_genai_client)

    client, error = text.get_gemini_client("fake_key")
    assert client == mock_genai_client

def test_text_chat_session(mocker):
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat

    chat = text.create_chat_session(mock_client)
    assert chat == mock_chat
    mock_client.chats.create.assert_called_once()
