import pytest
from modules.music import generate_music

def test_generate_music_success(mocker):
    # Mock get_music_client
    mock_client = mocker.MagicMock()
    # Mock the predict method to return a tuple (like the gradio client does)
    mock_client.predict.return_value = ("path/to/audio.wav",)

    mocker.patch("modules.music.get_music_client", return_value=(mock_client, None))

    audio_path, error = generate_music("happy song")

    assert error is None
    assert audio_path == "path/to/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    mocker.patch("modules.music.get_music_client", return_value=(None, "Init error"))

    audio_path, error = generate_music("test")

    assert audio_path is None
    assert error == "Init error"

def test_generate_music_predict_error(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.side_effect = Exception("Prediction failed")
    mocker.patch("modules.music.get_music_client", return_value=(mock_client, None))

    audio_path, error = generate_music("test")

    assert audio_path is None
    assert "Prediction failed" in error
