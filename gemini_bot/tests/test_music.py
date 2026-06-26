from modules.music import get_music_client, generate_music

def test_get_music_client_success(mocker):
    # Need to clear streamlit cache to test properly
    import streamlit as st
    st.cache_resource.clear()

    mock_client = mocker.patch("modules.music.Client")
    client, error = get_music_client()

    assert client is not None
    assert error is None
    mock_client.assert_called_once_with("sanchit-gandhi/musicgen-streaming")

def test_get_music_client_error(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mocker.patch("modules.music.Client", side_effect=Exception("Connection error"))
    client, error = get_music_client()

    assert client is None
    assert "Ошибка инициализации сервиса музыки" in error

def test_generate_music_no_client():
    path, error = generate_music("test", None)
    assert path is None
    assert error == "Клиент музыки не инициализирован."

def test_generate_music_success(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "path/to/music.wav"

    path, error = generate_music("rock song", mock_client)

    assert path == "path/to/music.wav"
    assert error is None
    mock_client.predict.assert_called_once_with(
        text_prompt="rock song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker):
    mock_client = mocker.Mock()
    mock_client.predict.side_effect = Exception("Generation failed")

    path, error = generate_music("test", mock_client)
    assert path is None
    assert "Ошибка при генерации музыки" in error
