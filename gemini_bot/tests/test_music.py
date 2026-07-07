from modules.music import generate_music, get_music_client
from unittest.mock import MagicMock

def test_get_music_client_success(mocker):
    # Mock gradio_client.Client
    mock_client = mocker.patch("modules.music.Client")
    client, error = get_music_client()

    assert client is not None
    assert error is None
    mock_client.assert_called_once_with("sanchit-gandhi/musicgen-streaming")

def test_generate_music_success(mocker):
    # Setup mock client
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = ("/tmp/audio.wav", "some_other_info")

    mocker.patch("modules.music.get_music_client", return_value=(mock_client_instance, None))

    path, error = generate_music("Тестовая мелодия")

    assert error is None
    assert path == "/tmp/audio.wav"
    mock_client_instance.predict.assert_called_once_with(
        text_prompt="Тестовая мелодия",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_string_return(mocker):
     # Setup mock client returning just string
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = "/tmp/audio2.wav"

    mocker.patch("modules.music.get_music_client", return_value=(mock_client_instance, None))

    path, error = generate_music("Тестовая мелодия 2")

    assert error is None
    assert path == "/tmp/audio2.wav"
