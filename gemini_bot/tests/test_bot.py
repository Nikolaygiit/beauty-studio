import pytest
from modules.routing import get_route, ROUTE_IMAGE, ROUTE_MUSIC, ROUTE_VIDEO, ROUTE_TEXT
from modules.text import get_gemini_client
from modules.music import generate_music
from modules.video import generate_video

def test_routing_image():
    assert get_route("Нарисуй красивый пейзаж") == ROUTE_IMAGE
    assert get_route("Сделай фото кота") == ROUTE_IMAGE
    assert get_route("Покажи изображение машины") == ROUTE_IMAGE

def test_routing_music():
    assert get_route("Сгенерируй музыку для релакса") == ROUTE_MUSIC
    assert get_route("Напиши песню про любовь") == ROUTE_MUSIC
    assert get_route("Включи крутой трек") == ROUTE_MUSIC

def test_routing_video():
    assert get_route("Создай видео с природой") == ROUTE_VIDEO
    assert get_route("Покажи ролик про животных") == ROUTE_VIDEO

def test_routing_text():
    assert get_route("Как дела?") == ROUTE_TEXT
    assert get_route("Расскажи сказку") == ROUTE_TEXT
    # False positive test to ensure short words are correctly handled
    assert get_route("Что такое фотосинтез?") == ROUTE_TEXT

def test_get_gemini_client_no_key():
    client, error = get_gemini_client("")
    assert client is None
    assert error == "API-ключ не предоставлен."

def test_generate_music_mocked(mocker):
    # Mock get_music_client to avoid real client initialization
    mock_client = mocker.MagicMock()
    # Gradio endpoint returns a tuple with the audio path as first element
    mock_client.predict.return_value = ("/fake/path/audio.wav",)

    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    audio_path, error = generate_music("Тестовая музыка")
    assert error is None
    assert audio_path == "/fake/path/audio.wav"
    mock_client.predict.assert_called_once()

def test_generate_video_mocked(mocker):
    mock_client = mocker.MagicMock()
    # Gradio endpoint returns a dict inside a tuple (often) or a string
    mock_client.predict.return_value = ({"video": "/fake/path/video.mp4"},)

    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    video_path, error = generate_video("Тестовое видео")
    assert error is None
    assert video_path == "/fake/path/video.mp4"
    mock_client.predict.assert_called_once()
