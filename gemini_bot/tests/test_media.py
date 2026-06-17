import pytest
from modules.music import generate_music
from modules.video import generate_video
from modules.image import generate_image

def test_generate_image_no_prompt():
    url, err = generate_image("")
    assert url is None
    assert "Prompt is required" in err

def test_generate_image_success():
    url, err = generate_image("test prompt")
    assert err is None
    assert url.startswith("https://image.pollinations.ai/prompt/test%20prompt")

def test_generate_music_no_prompt():
    url, err = generate_music("")
    assert url is None
    assert "Prompt is required" in err

def test_generate_music_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "fake_audio.wav"
    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    url, err = generate_music("test music prompt")
    assert err is None
    assert url == "fake_audio.wav"

def test_generate_video_no_prompt():
    url, err = generate_video("")
    assert url is None
    assert "Prompt is required" in err

def test_generate_video_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "fake_video.mp4"
    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    url, err = generate_video("test video prompt")
    assert err is None
    assert url == "fake_video.mp4"
