from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from modules.text import get_gemini_client

def test_generate_image():
    prompt = "Red apple"
    url, error = generate_image(prompt)
    assert url is not None
    assert "pollinations.ai" in url
    assert "Red%20apple" in url
    assert error is None

def test_get_gemini_client():
    # Empty API key
    client, error = get_gemini_client("")
    assert client is None
    assert error == "API-ключ не предоставлен."

def test_generate_music(mocker):
    # Patch the get_music_client function to avoid real network requests
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = ("/fake/path/audio.wav", None)

    mocker.patch('modules.music.get_music_client', return_value=mock_client_instance)

    path, error = generate_music("Test prompt")

    assert path == "/fake/path/audio.wav"
    assert error is None
    mock_client_instance.predict.assert_called_once_with(
        text_prompt="Test prompt",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_generate_video(mocker):
    # Patch the get_video_client function
    mock_client_instance = mocker.MagicMock()
    mock_client_instance.predict.return_value = {"video": "/fake/path/video.mp4"}

    mocker.patch('modules.video.get_video_client', return_value=mock_client_instance)

    path, error = generate_video("Test prompt")

    assert path == "/fake/path/video.mp4"
    assert error is None
    mock_client_instance.predict.assert_called_once_with(
        "Test prompt", -1, 16, 25, api_name="/generate_video"
    )
