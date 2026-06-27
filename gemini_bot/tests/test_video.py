from modules.video import generate_video, get_video_client
import pytest

@pytest.fixture
def mock_client(mocker):
    mock = mocker.MagicMock()
    mock.predict.return_value = {'video': 'mock_video_path.mp4'}
    return mock

def test_get_video_client_success(mocker, mock_client):
    mocker.patch('modules.video.Client', return_value=mock_client)
    # Clear cache to ensure we test the function logic
    get_video_client.clear()
    client, error = get_video_client()

    assert error is None
    assert client == mock_client

def test_get_video_client_error(mocker):
    mocker.patch('modules.video.Client', side_effect=ValueError("Invalid space"))
    get_video_client.clear()
    client, error = get_video_client()

    assert client is None
    assert "Ошибка инициализации видео клиента: Invalid space" in error

def test_generate_video_success(mocker, mock_client):
    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    result, error = generate_video("test prompt")

    assert error is None
    assert result == "mock_video_path.mp4"
    mock_client.predict.assert_called_once_with(
        "test prompt",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_generate_video_error(mocker, mock_client):
    mock_client.predict.side_effect = Exception("Generation Failed")
    mocker.patch('modules.video.get_video_client', return_value=(mock_client, None))

    result, error = generate_video("test prompt")

    assert result is None
    assert "Ошибка при создании видео: Generation Failed" in error
