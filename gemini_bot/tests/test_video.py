import pytest
from modules.video import get_video_client, generate_video

def test_generate_video_success_dict(mocker):
    # Mock get_video_client to return dict
    mock_client = mocker.Mock()
    mock_client.predict.return_value = {"video": "/path/to/video.mp4"}
    mocker.patch("modules.video.get_video_client", return_value=(mock_client, None))

    video_path, error = generate_video("человек идет по луне")

    assert video_path == "/path/to/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once()

def test_generate_video_success_str(mocker):
    # Mock get_video_client to return str
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "/path/to/video.mp4"
    mocker.patch("modules.video.get_video_client", return_value=(mock_client, None))

    video_path, error = generate_video("человек идет по луне")

    assert video_path == "/path/to/video.mp4"
    assert error is None

def test_generate_video_error(mocker):
    # Mock get_video_client to return an error
    mocker.patch("modules.video.get_video_client", return_value=(None, "Mock Video Init Error"))

    video_path, error = generate_video("человек идет по луне")

    assert video_path is None
    assert error == "Mock Video Init Error"
