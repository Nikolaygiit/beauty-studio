import pytest
import urllib.parse
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import create_chat_session

def test_generate_image_url_encoding():
    prompt = "кошка в космосе"
    image_url, err = generate_image(prompt)

    assert err is None
    assert "https://pollinations.ai/p/" in image_url
    assert urllib.parse.quote(prompt) in image_url
    assert "seed=" in image_url

def test_generate_music_success(mocker):
    # Mock get_music_client to return a mock client
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "/path/to/mocked_audio.wav"
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    prompt = "веселая песня"
    audio_path, err = generate_music(prompt)

    assert err is None
    assert audio_path == "/path/to/mocked_audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt=prompt,
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker):
    # Mock to raise an exception
    mock_client = mocker.Mock()
    mock_client.predict.side_effect = Exception("API error")
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    audio_path, err = generate_music("test")

    assert audio_path is None
    assert "Ошибка генерации музыки" in err

def test_generate_video_success_dict(mocker):
    mock_client = mocker.Mock()
    # Gradio might return a dict containing 'video'
    mock_client.predict.return_value = {"video": "/path/to/mocked_video.mp4"}
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    prompt = "кот бежит"
    video_path, err = generate_video(prompt)

    assert err is None
    assert video_path == "/path/to/mocked_video.mp4"
    mock_client.predict.assert_called_once_with(
        prompt,
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_success_string(mocker):
    mock_client = mocker.Mock()
    # Or Gradio might return just the string
    mock_client.predict.return_value = "/path/to/mocked_video2.mp4"
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    video_path, err = generate_video("test")
    assert err is None
    assert video_path == "/path/to/mocked_video2.mp4"

def test_generate_video_init_error(mocker):
    # Mock get_video_client to return error string
    mocker.patch("modules.video.get_video_client", return_value="Ошибка инициализации")

    video_path, err = generate_video("test")

    assert video_path is None
    assert err == "Ошибка инициализации"

def test_create_chat_session(mocker):
    mock_genai_client = mocker.Mock()
    mock_chat_session = mocker.Mock()

    mock_genai_client.chats.create.return_value = mock_chat_session
    mocker.patch("modules.text.genai.Client", return_value=mock_genai_client)

    client, session = create_chat_session("test_api_key")

    assert client == mock_genai_client
    assert session == mock_chat_session
    mock_genai_client.chats.create.assert_called_once()
