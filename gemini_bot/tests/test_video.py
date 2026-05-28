import pytest
from unittest.mock import patch, MagicMock
from modules.video import get_video_client, generate_video

def test_get_video_client_success():
    with patch('modules.video.Client') as MockClient:
        mock_client_instance = MagicMock()
        MockClient.return_value = mock_client_instance

        # Clear cache to ensure a fresh call
        get_video_client.clear()
        client, error = get_video_client()

        assert client is mock_client_instance
        assert error is None
        MockClient.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis", timeout=60)

def test_get_video_client_error():
    with patch('modules.video.Client') as MockClient:
        MockClient.side_effect = Exception("Test error")

        # Clear cache to ensure a fresh call
        get_video_client.clear()
        client, error = get_video_client()

        assert client is None
        assert "Test error" in error

def test_generate_video_success_string():
    with patch('modules.video.get_video_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.predict.return_value = "path/to/video.mp4"
        mock_get_client.return_value = (mock_client, None)

        path, error = generate_video("test prompt")
        assert path == "path/to/video.mp4"
        assert error is None

def test_generate_video_success_dict():
    with patch('modules.video.get_video_client') as mock_get_client:
        mock_client = MagicMock()
        mock_client.predict.return_value = {"video": "path/to/video.mp4"}
        mock_get_client.return_value = (mock_client, None)

        path, error = generate_video("test prompt")
        assert path == "path/to/video.mp4"
        assert error is None

def test_generate_video_client_error():
    with patch('modules.video.get_video_client') as mock_get_client:
        mock_get_client.return_value = (None, "Client error")

        path, error = generate_video("test prompt")
        assert path is None
        assert error == "Client error"
