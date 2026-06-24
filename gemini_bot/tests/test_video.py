import pytest
from modules.video import get_video_client, generate_video

def test_get_video_client_success(mocker):
    mocker.patch('modules.video.Client', return_value="mock_client")
    client, error = get_video_client()
    assert client == "mock_client"
    assert error is None

def test_generate_video_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/video.mp4"

    path, error = generate_video(mock_client, "test video")

    assert path == "/path/to/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once_with(
        "test video",
        -1,
        16,
        25,
        api_name="/generate_video"
    )
