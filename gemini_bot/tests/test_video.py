from modules.video import generate_video, get_video_client
from unittest.mock import MagicMock

def test_get_video_client_success(mocker):
    # Mock gradio_client.Client
    mock_client = mocker.patch("modules.video.Client")
    client, error = get_video_client()

    assert client is not None
    assert error is None
    mock_client.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis")

def test_generate_video_success_tuple(mocker):
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = ("/tmp/video.mp4",)

    mocker.patch("modules.video.get_video_client", return_value=(mock_client_instance, None))

    path, error = generate_video("Тестовое видео")

    assert error is None
    assert path == "/tmp/video.mp4"
    mock_client_instance.predict.assert_called_once_with(
        "Тестовое видео", -1, 16, 25, api_name="/generate_video"
    )

def test_generate_video_success_dict(mocker):
    mock_client_instance = MagicMock()
    mock_client_instance.predict.return_value = {"video": "/tmp/video2.mp4"}

    mocker.patch("modules.video.get_video_client", return_value=(mock_client_instance, None))

    path, error = generate_video("Тестовое видео 2")

    assert error is None
    assert path == "/tmp/video2.mp4"
