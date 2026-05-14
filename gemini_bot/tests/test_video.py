import pytest
from unittest.mock import MagicMock, patch
from modules.video import generate_video

@patch('modules.video.get_video_client')
def test_generate_video(mock_get_client):
    mock_client = MagicMock()
    mock_client.predict.return_value = "/tmp/video.mp4"
    mock_get_client.return_value = mock_client

    path, error = generate_video("dog running")

    assert error is None
    assert path == "/tmp/video.mp4"
    mock_client.predict.assert_called_once_with(
        "dog running",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

@patch('modules.video.get_video_client')
def test_generate_video_value_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.predict.side_effect = ValueError("Invalid input")
    mock_get_client.return_value = mock_client

    path, error = generate_video("invalid prompt")

    assert path is None
    assert "Ошибка API генерации видео" in error

@patch('modules.video.get_video_client')
def test_generate_video_runtime_error(mock_get_client):
    mock_client = MagicMock()
    mock_client.predict.side_effect = RuntimeError("GPU Out of Memory")
    mock_get_client.return_value = mock_client

    path, error = generate_video("complex prompt")

    assert path is None
    assert "Ошибка выполнения видео-модели" in error
