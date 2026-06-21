from modules.video import generate_video

def test_generate_video_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/mock_video.mp4"
    mocker.patch('modules.video.get_video_client', return_value=mock_client)

    path, error = generate_video("человек идет по улице")

    assert error is None
    assert path == "/path/to/mock_video.mp4"
    mock_client.predict.assert_called_once_with(
        "человек идет по улице",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_client_error(mocker):
    mocker.patch('modules.video.get_video_client', return_value="Ошибка инициализации")

    path, error = generate_video("человек идет по улице")

    assert path is None
    assert error == "Ошибка инициализации"
