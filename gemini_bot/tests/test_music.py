import pytest
from modules.music import get_music_client, generate_music

def test_get_music_client_success(mocker):
    mock_client = mocker.patch("modules.music.Client")
    client, err = get_music_client()
    mock_client.assert_called_once_with("sanchit-gandhi/musicgen-streaming")
    assert err is None
    assert client is not None

def test_get_music_client_failure(mocker):
    # clear cache before testing to force exception
    import streamlit as st
    st.cache_resource.clear()

    mocker.patch("modules.music.Client", side_effect=Exception("Connection Error"))
    client, err = get_music_client()
    assert client is None
    assert "Ошибка инициализации музыкального" in err

def test_generate_music_success(mocker):
    mock_get_client = mocker.patch("modules.music.get_music_client")
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = ["/path/to/audio.wav"]
    mock_get_client.return_value = (mock_client_instance, None)

    path, err = generate_music("happy song")

    mock_client_instance.predict.assert_called_once_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )
    assert path == "/path/to/audio.wav"
    assert err is None

def test_generate_music_error(mocker):
    mock_get_client = mocker.patch("modules.music.get_music_client")
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.side_effect = Exception("Prediction failed")
    mock_get_client.return_value = (mock_client_instance, None)

    path, err = generate_music("bad song")
    assert path is None
    assert "Ошибка генерации музыки" in err
