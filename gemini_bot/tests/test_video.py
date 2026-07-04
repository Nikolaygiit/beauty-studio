import pytest
from modules.video import generate_video

def test_generate_video_success(mocker):
    # Mock get_video_client
    mock_client = mocker.MagicMock()
    # Mock the predict method to return a string path
    mock_client.predict.return_value = "path/to/video.mp4"

    mocker.patch("modules.video.get_video_client", return_value=(mock_client, None))

    video_path, error = generate_video("a dog running")

    assert error is None
    assert video_path == "path/to/video.mp4"
    # Verify fixed parameters
    mock_client.predict.assert_called_once_with(
        "a dog running",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_client_error(mocker):
    mocker.patch("modules.video.get_video_client", return_value=(None, "Init error"))

    video_path, error = generate_video("test")

    assert video_path is None
    assert error == "Init error"
