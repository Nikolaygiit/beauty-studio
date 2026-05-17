from unittest.mock import Mock
from modules.video import generate_video

def test_generate_video_success():
    mock_client = Mock()
    mock_client.predict.return_value = ("/path/to/video.mp4", "some_other_data")

    prompt = "кошка ловит мышь"
    video_path, err = generate_video(mock_client, prompt)

    assert err is None
    assert video_path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once_with(prompt, -1, 16, 25, api_name="/generate_video")

def test_generate_video_error():
    mock_client = Mock()
    mock_client.predict.side_effect = Exception("API error")

    prompt = "кошка ловит мышь"
    video_path, err = generate_video(mock_client, prompt)

    assert video_path is None
    assert "API error" in err
    mock_client.predict.assert_called_once_with(prompt, -1, 16, 25, api_name="/generate_video")
