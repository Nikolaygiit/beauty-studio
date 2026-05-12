import pytest
from unittest.mock import patch
from modules.music import generate_music

@patch("modules.music.Client")
def test_generate_music_success(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_instance.predict.return_value = "/tmp/fake_audio.wav"

    with patch("os.path.exists", return_value=True):
        audio_path, error = generate_music("test prompt")

    assert error is None
    assert audio_path == "/tmp/fake_audio.wav"

@patch("modules.music.Client")
def test_generate_music_failure_not_found(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_instance.predict.return_value = "/tmp/fake_audio.wav"

    with patch("os.path.exists", return_value=False):
        audio_path, error = generate_music("test prompt")

    assert audio_path is None
    assert "не найден" in error
