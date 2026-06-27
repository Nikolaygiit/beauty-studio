from modules.text import get_gemini_client

def test_get_gemini_client_success(mocker):
    mock_client_instance = mocker.MagicMock()
    mocker.patch('google.genai.Client', return_value=mock_client_instance)

    client, error = get_gemini_client("fake_api_key")

    assert error is None
    assert client == mock_client_instance

def test_get_gemini_client_error(mocker):
    mocker.patch('google.genai.Client', side_effect=Exception("API Error"))

    client, error = get_gemini_client("fake_api_key")

    assert client is None
    assert "Ошибка инициализации Gemini: API Error" in error
