from modules.music import generate_music

def test_generate_music_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/mock_audio.wav"
    mocker.patch('modules.music.get_music_client', return_value=mock_client)

    path, error = generate_music("веселая мелодия")

    assert error is None
    assert path == "/path/to/mock_audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="веселая мелодия",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_client_error(mocker):
    mocker.patch('modules.music.get_music_client', return_value="Ошибка инициализации")

    path, error = generate_music("веселая мелодия")

    assert path is None
    assert error == "Ошибка инициализации"
