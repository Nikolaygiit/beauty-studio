import pytest
from modules.routing import get_route
from modules.image import generate_image

def test_routing():
    assert get_route("Нарисуй мне красивый пейзаж") == "image"
    assert get_route("Сделай фото кота") == "image"
    assert get_route("Включи песню") == "music"
    assert get_route("Создай трек") == "music"
    assert get_route("Сделай видео") == "video"
    assert get_route("Покажи ролик") == "video"
    assert get_route("Как дела?") == "text"
    assert get_route("Расскажи о себе") == "text"

def test_image_generation():
    url, error = generate_image("кот")
    assert error is None
    assert "https://image.pollinations.ai/prompt/" in url
    assert "nologo=true" in url

# Тестирование моков для Gradio и Gemini
def test_music_generation_mock(mocker):
    # Мокаем get_music_client
    mock_client = mocker.patch("modules.music.get_music_client")
    mock_instance = mock_client.return_value
    mock_instance.predict.return_value = "/tmp/fake_audio.wav"

    from modules.music import generate_music
    result, error = generate_music("крутая песня")

    assert error is None
    assert result == "/tmp/fake_audio.wav"
    mock_instance.predict.assert_called_once()

def test_video_generation_mock(mocker):
    # Мокаем get_video_client
    mock_client = mocker.patch("modules.video.get_video_client")
    mock_instance = mock_client.return_value
    mock_instance.predict.return_value = "/tmp/fake_video.mp4"

    from modules.video import generate_video
    result, error = generate_video("смешное видео")

    assert error is None
    assert result == "/tmp/fake_video.mp4"
    mock_instance.predict.assert_called_once()

def test_gemini_client_mock(mocker):
    # Мокаем genai.Client
    mock_genai_client = mocker.patch("modules.text.genai.Client")
    mock_instance = mock_genai_client.return_value
    mock_chat = mocker.Mock()
    mock_instance.chats.create.return_value = mock_chat

    from modules.text import init_gemini_client
    client, chat, error = init_gemini_client("fake_key")

    assert error is None
    assert client == mock_instance
    assert chat == mock_chat
    mock_genai_client.assert_called_once_with(api_key="fake_key")
