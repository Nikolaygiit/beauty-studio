import pytest
from unittest.mock import patch, MagicMock
from modules.music import get_music_client, generate_music

def test_get_music_client_success():
    with patch('modules.music.Client') as MockClient:
        mock_client_instance = MagicMock()
        MockClient.return_value = mock_client_instance

        # Clear cache to ensure a fresh call
        get_music_client.clear()
        client, error = get_music_client()

        assert client is mock_client_instance
        assert error is None
        MockClient.assert_called_once_with("sanchit-gandhi/musicgen-streaming", timeout=60)

def test_get_music_client_error():
    with patch('modules.music.Client') as MockClient:
        MockClient.side_effect = Exception("Test error")

        # Clear cache to ensure a fresh call
        get_music_client.clear()
        client, error = get_music_client()

        assert client is None
        assert "Test error" in error

def test_generate_music_success():
    with patch('modules.music.get_music_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.predict.return_value = ("path/to/music.mp3", "other_data")
        mock_get_client.return_value = (mock_client, None)

        path, error = generate_music("test prompt")
        assert path == "path/to/music.mp3"
        assert error is None
        mock_client.predict.assert_called_once()

def test_generate_music_client_error():
    with patch('modules.music.get_music_client') as mock_get_client:
        mock_get_client.return_value = (None, "Client error")

        path, error = generate_music("test prompt")
        assert path is None
        assert error == "Client error"

def test_generate_music_predict_error():
    with patch('modules.music.get_music_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.predict.side_effect = Exception("Predict error")
        mock_get_client.return_value = (mock_client, None)

        path, error = generate_music("test prompt")
        assert path is None
        assert "Predict error" in error
