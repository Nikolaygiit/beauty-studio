from modules.music import generate_music

def test_generate_music_mocked(mocker):
    # Mock the get_music_client to return a dummy client
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/fake_audio.wav"
    mocker.patch('modules.music.get_music_client', return_value=mock_client)

    path, error = generate_music("Тестовая музыка")
    assert error is None
    assert path == "/path/to/fake_audio.wav"
