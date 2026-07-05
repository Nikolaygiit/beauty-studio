import pytest
from modules.music import get_music_client, generate_music
from gradio_client import Client

def test_get_music_client_success(mocker):
    # Mocking Client initialization
    mock_client_instance = mocker.Mock(spec=Client)
    mocker.patch('modules.music.Client', return_value=mock_client_instance)

    # Need to clear cache to allow testing initialization
    get_music_client.clear()

    client, error = get_music_client()

    assert client is not None
    assert error is None

def test_get_music_client_failure(mocker):
    # Mocking Client to raise exception
    mocker.patch('modules.music.Client', side_effect=Exception("Connection error"))

    get_music_client.clear()

    client, error = get_music_client()

    assert client is None
    assert "Ошибка при подключении к сервису музыки: Connection error" in error

def test_generate_music_success(mocker):
    mock_client = mocker.Mock(spec=Client)
    mock_client.predict.return_value = "/path/to/audio.mp3"

    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    path, error = generate_music("test prompt")

    assert error is None
    assert path == "/path/to/audio.mp3"
    mock_client.predict.assert_called_once_with(
        text_prompt="test prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    mocker.patch('modules.music.get_music_client', return_value=(None, "Init error"))

    path, error = generate_music("test prompt")

    assert path is None
    assert error == "Init error"

def test_generate_music_predict_error(mocker):
    mock_client = mocker.Mock(spec=Client)
    mock_client.predict.side_effect = Exception("Predict error")

    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    path, error = generate_music("test prompt")

    assert path is None
    assert "Ошибка при генерации музыки: Predict error" in error
