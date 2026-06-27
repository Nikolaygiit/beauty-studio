from modules.music import generate_music, get_music_client
import pytest

@pytest.fixture
def mock_client(mocker):
    mock = mocker.MagicMock()
    mock.predict.return_value = "mock_audio_path.wav"
    return mock

def test_get_music_client_success(mocker, mock_client):
    mocker.patch('modules.music.Client', return_value=mock_client)
    client, error = get_music_client()

    assert error is None
    assert client == mock_client

def test_get_music_client_error(mocker):
    mocker.patch('modules.music.Client', side_effect=Exception("API Error"))
    # Clear cache to ensure it runs
    get_music_client.clear()
    client, error = get_music_client()

    assert client is None
    assert "Ошибка инициализации музыкального клиента: API Error" in error

def test_generate_music_success(mocker, mock_client):
    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    result, error = generate_music("test prompt")

    assert error is None
    assert result == "mock_audio_path.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="test prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_music_error(mocker, mock_client):
    mock_client.predict.side_effect = Exception("Generation Error")
    mocker.patch('modules.music.get_music_client', return_value=(mock_client, None))

    result, error = generate_music("test prompt")

    assert result is None
    assert "Ошибка при создании музыки: Generation Error" in error
