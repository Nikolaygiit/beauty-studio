import pytest
from unittest.mock import MagicMock, patch
from modules.music import generate_music

@patch('modules.music.get_music_client')
def test_generate_music(mock_get_client):
    mock_client = MagicMock()
    # Mock behavior of tuple return from Gradio predict for musicgen
    mock_client.predict.return_value = ("/tmp/audio.wav", "/tmp/audio.wav")
    mock_get_client.return_value = mock_client

    path, error = generate_music("happy song")

    assert error is None
    assert path == "/tmp/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

@patch('modules.music.get_music_client')
def test_generate_music_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.predict.side_effect = Exception("API Error")
    mock_get_client.return_value = mock_client

    path, error = generate_music("sad song")

    assert path is None
    assert "Ошибка при генерации музыки" in error
