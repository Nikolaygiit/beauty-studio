from modules.music import generate_music

def test_generate_music_success(mocker):
    # Mock get_music_client to return a mock client
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/audio.wav"

    mocker.patch('modules.music.get_music_client', return_value=mock_client)

    audio_path, error = generate_music("веселая мелодия")

    assert error is None
    assert audio_path == "/path/to/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="веселая мелодия",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    # Simulate get_music_client returning an error string
    mocker.patch('modules.music.get_music_client', return_value="Failed to connect")

    audio_path, error = generate_music("test")

    assert audio_path is None
    assert "Ошибка инициализации клиента: Failed to connect" in error
