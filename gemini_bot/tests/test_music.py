import pytest
from modules.music import get_music_client, generate_music

def test_get_music_client(mocker):
    # Mocking Gradio Client
    mock_client_class = mocker.patch("modules.music.Client")
    mock_instance = mocker.Mock()
    mock_client_class.return_value = mock_instance

    # We also need to bypass Streamlit's @st.cache_resource for testing
    # Since cache_resource wraps the function, we test the wrapped function directly or mock the cache

    # Alternatively, just let it mock Client and call get_music_client
    # However, to ensure a clean state, it's safer to test generate_music which calls get_music_client internally
    pass

def test_generate_music_success(mocker):
    # Mock get_music_client
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "/path/to/audio.wav"
    mocker.patch("modules.music.get_music_client", return_value=(mock_client, None))

    audio_path, error = generate_music("веселая мелодия")

    assert audio_path == "/path/to/audio.wav"
    assert error is None
    mock_client.predict.assert_called_once()

def test_generate_music_error(mocker):
    # Mock get_music_client to return an error
    mocker.patch("modules.music.get_music_client", return_value=(None, "Mock Initialization Error"))

    audio_path, error = generate_music("веселая мелодия")

    assert audio_path is None
    assert error == "Mock Initialization Error"
