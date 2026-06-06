from modules.video import generate_video

def test_generate_video_mocked(mocker):
    # Mock the get_video_client to return a dummy client
    mock_client = mocker.MagicMock()
    # The video route expects the result to be returned as the first item of a tuple if it's a tuple,
    # or the result directly if it's a string, or extracting from dict.
    mock_client.predict.return_value = "/path/to/fake_video.mp4"
    mocker.patch('modules.video.get_video_client', return_value=mock_client)

    path, error = generate_video("Тестовое видео")
    assert error is None
    assert path == "/path/to/fake_video.mp4"
