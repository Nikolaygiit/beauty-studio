import pytest
from modules.music import get_music_client, generate_music

def test_get_music_client_success(mocker):
    mocker.patch('modules.music.Client', return_value="mock_client")
    client, error = get_music_client()
    assert client == "mock_client"
    assert error is None

def test_generate_music_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = ("/path/to/audio.wav", "meta")

    path, error = generate_music(mock_client, "test music")

    assert path == "/path/to/audio.wav"
    assert error is None
    mock_client.predict.assert_called_once_with(
        text_prompt="test music",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )
