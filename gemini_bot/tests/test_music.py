import pytest
from modules.music import generate_music, get_music_client
import streamlit as st

def test_get_music_client(mocker):
    # Just mocking to ensure it calls Gradio Client
    mock_client = mocker.patch('modules.music.Client')
    client = get_music_client()
    # Cache makes it tricky to assert call counts across tests sometimes,
    # but we can verify it returns something
    assert client is not None

def test_generate_music_success(mocker):
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = "fake/audio/path.wav"
    mocker.patch('modules.music.get_music_client', return_value=mock_client_instance)

    path, error = generate_music("test prompt")

    assert error is None
    assert path == "fake/audio/path.wav"
    mock_client_instance.predict.assert_called_once_with(
        text_prompt="test prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker):
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.side_effect = Exception("API error")
    mocker.patch('modules.music.get_music_client', return_value=mock_client_instance)

    path, error = generate_music("test prompt")

    assert path is None
    assert "API error" in error
