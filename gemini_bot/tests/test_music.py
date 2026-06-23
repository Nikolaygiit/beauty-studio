from modules.music import get_music_client, generate_music

def test_get_music_client_success(mocker):
    mock_client_class = mocker.patch("modules.music.Client")
    mock_instance = mocker.Mock()
    mock_client_class.return_value = mock_instance

    client, err = get_music_client()
    assert err is None
    assert client == mock_instance
    mock_client_class.assert_called_once_with("sanchit-gandhi/musicgen-streaming")

def test_generate_music_success(mocker):
    # Mock the client initialization
    mock_client_instance = mocker.Mock()
    mock_get_client = mocker.patch("modules.music.get_music_client", return_value=(mock_client_instance, None))

    mock_client_instance.predict.return_value = "/path/to/audio.wav"

    audio_path, err = generate_music("happy song")

    assert err is None
    assert audio_path == "/path/to/audio.wav"
    mock_client_instance.predict.assert_called_once_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    mock_get_client = mocker.patch("modules.music.get_music_client", return_value=(None, "Initialization error"))

    audio_path, err = generate_music("happy song")

    assert audio_path is None
    assert err == "Initialization error"
