import pytest
from unittest.mock import MagicMock

from modules.text import create_client, create_chat_session, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Image Tests ---
def test_generate_image():
    url, err = generate_image("test prompt")
    assert url is not None
    assert err is None
    assert "image.pollinations.ai" in url
    assert "test%20prompt" in url

# --- Text Tests ---
def test_create_client_and_session(mocker):
    mock_genai = mocker.patch("modules.text.genai")

    mock_client_instance = MagicMock()
    mock_genai.Client.return_value = mock_client_instance

    client = create_client("fake_key")
    mock_genai.Client.assert_called_once_with(api_key="fake_key")

    mock_chat_session = MagicMock()
    mock_client_instance.chats.create.return_value = mock_chat_session

    session = create_chat_session(client)
    mock_client_instance.chats.create.assert_called_once()
    assert session == mock_chat_session

def test_generate_text_stream():
    mock_session = MagicMock()

    # Mocking the stream chunks
    chunk1 = MagicMock()
    chunk1.text = "Hello "
    chunk2 = MagicMock()
    chunk2.text = "World"

    mock_session.send_message_stream.return_value = [chunk1, chunk2]

    chunks = list(generate_text_stream(mock_session, "prompt"))
    assert chunks == ["Hello ", "World"]

# --- Music Tests ---
def test_generate_music_success(mocker):
    mock_client_constructor = mocker.patch("modules.music.get_music_client")
    mock_gradio_client = MagicMock()
    mock_client_constructor.return_value = mock_gradio_client

    mock_gradio_client.predict.return_value = "/path/to/audio.wav"

    path, err = generate_music("happy song")

    assert path == "/path/to/audio.wav"
    assert err is None
    mock_gradio_client.predict.assert_called_once()

def test_generate_music_client_error(mocker):
    mock_client_constructor = mocker.patch("modules.music.get_music_client")
    mock_client_constructor.return_value = "Ошибка инициализации Musicgen: test error"

    path, err = generate_music("test")
    assert path is None
    assert err == "Ошибка инициализации Musicgen: test error"

def test_generate_music_predict_error(mocker):
    mock_client_constructor = mocker.patch("modules.music.get_music_client")
    mock_gradio_client = MagicMock()
    mock_client_constructor.return_value = mock_gradio_client

    mock_gradio_client.predict.side_effect = Exception("API fail")

    path, err = generate_music("test")
    assert path is None
    assert "Ошибка при генерации музыки" in err

# --- Video Tests ---
def test_generate_video_success(mocker):
    mock_client_constructor = mocker.patch("modules.video.get_video_client")
    mock_gradio_client = MagicMock()
    mock_client_constructor.return_value = mock_gradio_client

    mock_gradio_client.predict.return_value = {"video": "/path/to/video.mp4"}

    path, err = generate_video("cool video")

    assert path == "/path/to/video.mp4"
    assert err is None
    mock_gradio_client.predict.assert_called_once()

def test_generate_video_success_string_return(mocker):
    mock_client_constructor = mocker.patch("modules.video.get_video_client")
    mock_gradio_client = MagicMock()
    mock_client_constructor.return_value = mock_gradio_client

    mock_gradio_client.predict.return_value = "/path/to/video.mp4"

    path, err = generate_video("cool video")

    assert path == "/path/to/video.mp4"
    assert err is None

def test_generate_video_client_error(mocker):
    mock_client_constructor = mocker.patch("modules.video.get_video_client")
    mock_client_constructor.return_value = "Ошибка инициализации Video: test error"

    path, err = generate_video("test")
    assert path is None
    assert err == "Ошибка инициализации Video: test error"
