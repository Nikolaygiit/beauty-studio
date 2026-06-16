from modules.video import generate_video

def test_generate_video_success(mocker):
    # Mock get_video_client to return a mock client
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = {"video": "/path/to/video.mp4"}

    mocker.patch('modules.video.get_video_client', return_value=mock_client)

    video_path, error = generate_video("летящая птица")

    assert error is None
    assert video_path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once_with(
        "летящая птица",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_predict_error(mocker):
    # Mock client where predict raises an exception
    mock_client = mocker.MagicMock()
    mock_client.predict.side_effect = ValueError("Invalid prompt")

    mocker.patch('modules.video.get_video_client', return_value=mock_client)

    video_path, error = generate_video("test")

    assert video_path is None
    assert "Ошибка генерации видео: Invalid prompt" in error
