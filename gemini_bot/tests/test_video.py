import pytest
from modules.video import get_video_client, generate_video

def test_generate_video_empty_prompt():
    path, error = generate_video("")
    assert path is None
    assert "Prompt cannot be empty" in error

def test_generate_video_success(mocker):
    # Mock the get_video_client to return a mock client
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "/path/to/generated/video.mp4"
    mocker.patch("modules.video.get_video_client", return_value=(mock_client, None))

    path, error = generate_video("A flying car")
    assert path == "/path/to/generated/video.mp4"
    assert error is None
    mock_client.predict.assert_called_once_with(
        "A flying car",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_client_error(mocker):
    # Mock get_video_client to return an error
    mocker.patch("modules.video.get_video_client", return_value=(None, "Initialization failed"))

    path, error = generate_video("A flying car")
    assert path is None
    assert error == "Initialization failed"
