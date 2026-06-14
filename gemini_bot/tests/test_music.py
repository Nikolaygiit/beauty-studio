from modules.music import generate_music

def test_generate_music_success(mocker):
    mock_get_client = mocker.patch('modules.music.get_music_client')
    mock_client = mock_get_client.return_value
    mock_client.predict.return_value = "path/to/audio.mp3"

    path, error = generate_music("test prompt")

    assert path == "path/to/audio.mp3"
    assert error is None
    mock_client.predict.assert_called_once_with(
        text_prompt="test prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_exception(mocker):
    mock_get_client = mocker.patch('modules.music.get_music_client')
    mock_client = mock_get_client.return_value
    mock_client.predict.side_effect = Exception("Connection error")

    path, error = generate_music("test prompt")

    assert path is None
    assert "Ошибка при генерации музыки: Connection error" in error
