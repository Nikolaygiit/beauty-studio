import pytest
import urllib.parse
from gemini_bot.modules.image import generate_image
from gemini_bot.modules.music import generate_music
from gemini_bot.modules.video import generate_video
from gemini_bot.modules.text import init_gemini, generate_text_stream

def test_generate_image(mocker):
    prompt = "Тестовый запрос"
    mocker.patch('random.randint', return_value=123)
    url, err = generate_image(prompt)
    encoded = urllib.parse.quote(prompt)
    assert url == f"https://image.pollinations.ai/prompt/{encoded}?seed=123&nologo=true"
    assert err is None

def test_generate_music(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.return_value = ("/tmp/audio.wav",)
    mocker.patch('gemini_bot.modules.music.get_music_client', return_value=mock_client)

    path, err = generate_music("Тестовая музыка")
    assert path == "/tmp/audio.wav"
    assert err is None
    mock_client.predict.assert_called_once_with(
        text_prompt="Тестовая музыка",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_video(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.return_value = {"video": "/tmp/video.mp4"}
    mocker.patch('gemini_bot.modules.video.get_video_client', return_value=mock_client)

    path, err = generate_video("Тестовое видео")
    assert path == "/tmp/video.mp4"
    assert err is None
    mock_client.predict.assert_called_once_with(
        "Тестовое видео", -1, 16, 25, api_name="/generate_video"
    )

def test_generate_text_stream(mocker):
    mock_session = mocker.Mock()

    class MockChunk:
        def __init__(self, text):
            self.text = text

    mock_session.send_message_stream.return_value = [MockChunk("Привет"), MockChunk(", "), MockChunk("мир!")]

    chunks = list(generate_text_stream(mock_session, "Скажи привет"))
    assert chunks == ["Привет", ", ", "мир!"]
