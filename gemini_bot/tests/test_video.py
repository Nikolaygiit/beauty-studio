import pytest
from unittest.mock import patch
from modules.video import generate_video

@patch("modules.video.Client")
def test_generate_video_success_dict(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_instance.predict.return_value = {"video": "/tmp/fake_video.mp4"}

    with patch("os.path.exists", return_value=True):
        video_path, error = generate_video("test prompt")

    assert error is None
    assert video_path == "/tmp/fake_video.mp4"

@patch("modules.video.Client")
def test_generate_video_success_tuple(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_instance.predict.return_value = ("/tmp/fake_video2.mp4", "other data")

    with patch("os.path.exists", return_value=True):
        video_path, error = generate_video("test prompt")

    assert error is None
    assert video_path == "/tmp/fake_video2.mp4"

@patch("modules.video.Client")
def test_generate_video_error_handling(mock_client_class):
    mock_instance = mock_client_class.return_value
    mock_instance.predict.side_effect = ValueError("Invalid parameters")

    video_path, error = generate_video("test prompt")

    assert video_path is None
    assert "Ошибка значения" in error
