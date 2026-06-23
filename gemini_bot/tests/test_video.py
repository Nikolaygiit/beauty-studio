from modules.video import get_video_client, generate_video

def test_get_video_client_success(mocker):
    mock_client_class = mocker.patch("modules.video.Client")
    mock_instance = mocker.Mock()
    mock_client_class.return_value = mock_instance

    client, err = get_video_client()
    assert err is None
    assert client == mock_instance
    mock_client_class.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis")

def test_generate_video_success(mocker):
    mock_client_instance = mocker.Mock()
    mock_get_client = mocker.patch("modules.video.get_video_client", return_value=(mock_client_instance, None))

    mock_client_instance.predict.return_value = {"video": "/path/to/video.mp4"}

    video_path, err = generate_video("a running dog")

    assert err is None
    assert video_path == "/path/to/video.mp4"
    mock_client_instance.predict.assert_called_once_with(
        "a running dog",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_string_result(mocker):
    mock_client_instance = mocker.Mock()
    mock_get_client = mocker.patch("modules.video.get_video_client", return_value=(mock_client_instance, None))

    mock_client_instance.predict.return_value = "/path/to/video.mp4"

    video_path, err = generate_video("a running dog")

    assert err is None
    assert video_path == "/path/to/video.mp4"

def test_generate_video_client_error(mocker):
    mock_get_client = mocker.patch("modules.video.get_video_client", return_value=(None, "Initialization error"))

    video_path, err = generate_video("a running dog")

    assert video_path is None
    assert err == "Initialization error"
