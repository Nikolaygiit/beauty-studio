import pytest
from unittest.mock import MagicMock
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import init_chat_session, generate_text_stream

def test_generate_image():
    url, err = generate_image("test prompt")
    assert "image.pollinations.ai" in url
    assert "test%20prompt" in url
    assert err == ""

def test_generate_music(mocker):
    # Мок возвращаемого значения Client.predict
    mock_client = MagicMock()
    mock_client.predict.return_value = "mocked_audio.wav"

    # Мокаем get_music_client, чтобы не делать реальный запрос
    mocker.patch('modules.music.get_music_client', return_value=(mock_client, ""))

    res, err = generate_music("test music")
    assert res == "mocked_audio.wav"
    assert err == ""

def test_generate_video(mocker):
    # Мок возвращаемого значения Client.predict
    mock_client = MagicMock()
    mock_client.predict.return_value = {"video": "mocked_video.mp4"}

    mocker.patch('modules.video.get_video_client', return_value=(mock_client, ""))

    res, err = generate_video("test video")
    assert res == "mocked_video.mp4"
    assert err == ""

def test_generate_text_stream(mocker):
    mock_session = MagicMock()
    mock_chunk = MagicMock()
    mock_chunk.text = "Hello"
    mock_session.send_message_stream.return_value = [mock_chunk]

    generator = generate_text_stream(mock_session, "Hi")
    result = list(generator)
    assert result == ["Hello"]

def test_init_chat_session(mocker):
    mock_client_class = mocker.patch('modules.text.genai.Client')
    mock_client_instance = mock_client_class.return_value
    mock_client_instance.chats.create.return_value = "mock_session"

    client, session = init_chat_session("fake_key")

    assert client == mock_client_instance
    assert session == "mock_session"
    mock_client_instance.chats.create.assert_called_once()
