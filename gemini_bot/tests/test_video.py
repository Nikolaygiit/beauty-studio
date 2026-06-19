import pytest
from modules.video import generate_video, get_video_client

def test_generate_video_success_dict(mocker):
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = {'video': 'fake/video.mp4'}
    mocker.patch('modules.video.get_video_client', return_value=mock_client_instance)

    path, error = generate_video("test")

    assert error is None
    assert path == "fake/video.mp4"

def test_generate_video_success_str(mocker):
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = 'fake/video.mp4'
    mocker.patch('modules.video.get_video_client', return_value=mock_client_instance)

    path, error = generate_video("test")

    assert error is None
    assert path == "fake/video.mp4"

def test_generate_video_error(mocker):
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.side_effect = RuntimeError("GPU error")
    mocker.patch('modules.video.get_video_client', return_value=mock_client_instance)

    path, error = generate_video("test")

    assert path is None
    assert "GPU error" in error
