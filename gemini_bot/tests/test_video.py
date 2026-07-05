import pytest
from modules.video import get_video_client, generate_video
from gradio_client import Client

def test_get_video_client_success(mocker):
    # Mocking Client initialization
    mock_client_instance = mocker.Mock(spec=Client)
    mocker.patch('modules.video.Client', return_value=mock_client_instance)

    get_video_client.clear()

    client, error = get_video_client()

    assert client is not None
    assert error is None

def test_get_video_client_failure(mocker):
    # Mocking Client to raise exception
    mocker.patch('modules.video.Client', side_effect=Exception("Connection error"))

    get_video_client.clear()

    client, error = get_video_client()

    assert client is None
    assert "Ошибка при подключении к сервису видео: Connection error" in error

def test_generate_video_success(mocker):
    mock_client = mocker.Mock(spec=Client)
    mock_client.predict.return_value = "/path/to/video.mp4"

    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    path, error = generate_video("test prompt")

    assert error is None
    assert path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once_with(
        "test prompt",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_client_error(mocker):
    mocker.patch('modules.video.get_video_client', return_value=(None, "Init error"))

    path, error = generate_video("test prompt")

    assert path is None
    assert error == "Init error"

def test_generate_video_predict_error(mocker):
    mock_client = mocker.Mock(spec=Client)
    mock_client.predict.side_effect = Exception("Predict error")

    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    path, error = generate_video("test prompt")

    assert path is None
    assert "Ошибка при генерации видео: Predict error" in error
