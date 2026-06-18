import pytest
import urllib.parse
from unittest.mock import MagicMock

# Import modules to test
from modules.routing import get_route
from modules.image import generate_image
from modules.music import generate_music, get_music_client
from modules.video import generate_video, get_video_client
from modules.text import get_client, initialize_chat_session, generate_text_stream

# Test Routing
def test_routing():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("сгенерируй фото собаки") == "image"
    assert get_route("Хочу послушать песню про лето") == "music"
    assert get_route("создай трек") == "music"
    assert get_route("Сделай видео космоса") == "video"
    assert get_route("сними ролик") == "video"
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи сказку") == "text"

# Test Image Module
def test_generate_image():
    prompt = "Test prompt"
    url, error = generate_image(prompt)
    assert error is None
    assert "image.pollinations.ai" in url
    assert urllib.parse.quote(prompt) in url
    assert "seed=" in url

# Test Music Module
def test_generate_music(mocker):
    # Mock the Gradio Client
    mock_client = MagicMock()
    mock_client.predict.return_value = "mock_music_path.wav"
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    result, error = generate_music("test music")
    assert error is None
    assert result == "mock_music_path.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="test music",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker):
    mocker.patch("modules.music.get_music_client", return_value="Error loading client")
    result, error = generate_music("test")
    assert result is None
    assert error == "Error loading client"

# Test Video Module
def test_generate_video(mocker):
    mock_client = MagicMock()
    mock_client.predict.return_value = "mock_video_path.mp4"
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    result, error = generate_video("test video")
    assert error is None
    assert result == "mock_video_path.mp4"
    mock_client.predict.assert_called_once_with(
        "test video", -1, 16, 25, api_name="/generate_video"
    )

def test_generate_video_error(mocker):
    mocker.patch("modules.video.get_video_client", return_value="Error loading client")
    result, error = generate_video("test")
    assert result is None
    assert error == "Error loading client"

# Test Text Module
def test_get_client_empty_key():
    assert get_client("") is None
    assert get_client(None) is None

def test_initialize_chat_session_no_client():
    assert initialize_chat_session(None) is None

def test_generate_text_stream_no_session():
    generator = generate_text_stream(None, "test")
    result = list(generator)
    assert result == ["Ошибка: Сессия чата не инициализирована."]

def test_generate_text_stream_success(mocker):
    mock_session = MagicMock()
    mock_chunk1 = MagicMock()
    mock_chunk1.text = "Hello "
    mock_chunk2 = MagicMock()
    mock_chunk2.text = "world!"
    mock_session.send_message_stream.return_value = [mock_chunk1, mock_chunk2]

    generator = generate_text_stream(mock_session, "Say hello")
    result = list(generator)

    assert result == ["Hello ", "world!"]
    mock_session.send_message_stream.assert_called_once_with("Say hello")

def test_generate_text_stream_exception(mocker):
    mock_session = MagicMock()
    mock_session.send_message_stream.side_effect = Exception("API Error")

    generator = generate_text_stream(mock_session, "Say hello")
    result = list(generator)

    assert result == ["\n\nПроизошла ошибка при генерации ответа: API Error"]
