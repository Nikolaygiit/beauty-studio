from modules.video import generate_video

def test_generate_video_success(mocker):
    mock_get_client = mocker.patch('modules.video.get_video_client')
    mock_client = mocker.MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.predict.return_value = "path/to/video.mp4"

    path, error = generate_video("test video prompt")

    assert path == "path/to/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once_with(
        "test video prompt",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_init_error(mocker):
    mock_get_client = mocker.patch('modules.video.get_video_client')
    # If get_video_client returns an error string
    mock_get_client.return_value = "Ошибка инициализации клиента: Not Found"

    path, error = generate_video("test video prompt")

    assert path is None
    assert error == "Ошибка инициализации клиента: Not Found"

def test_generate_video_exception(mocker):
    mock_get_client = mocker.patch('modules.video.get_video_client')
    mock_client = mocker.MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.predict.side_effect = Exception("Timeout error")

    path, error = generate_video("test prompt")

    assert path is None
    assert "Ошибка при генерации видео: Timeout error" in error
