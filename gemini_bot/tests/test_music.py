import pytest
from modules.music import get_music_client, generate_music

def test_generate_music_empty_prompt():
    path, error = generate_music("")
    assert path is None
    assert "Prompt cannot be empty" in error

def test_generate_music_success(mocker):
    # Mock the get_music_client to return a mock client
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/generated/audio.wav"
    mocker.patch("modules.music.get_music_client", return_value=(mock_client, None))

    path, error = generate_music("A happy tune")
    assert path == "/path/to/generated/audio.wav"
    assert error is None
    mock_client.predict.assert_called_once_with(
        text_prompt="A happy tune",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    # Mock get_music_client to return an error
    mocker.patch("modules.music.get_music_client", return_value=(None, "Initialization failed"))

    path, error = generate_music("A happy tune")
    assert path is None
    assert error == "Initialization failed"
