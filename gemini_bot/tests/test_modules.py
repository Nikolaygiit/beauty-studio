import pytest
from unittest.mock import patch, MagicMock

# Import functions to test
from modules.image import generate_image_url
from modules.music import generate_music, get_music_client
from modules.video import generate_video, get_video_client

def test_image_generation_url():
    """Test that image URL is constructed correctly."""
    prompt = "a cute cat"
    url, err = generate_image_url(prompt)

    assert err is None
    assert url is not None
    assert "https://image.pollinations.ai/prompt/a%20cute%20cat" in url
    assert "seed=" in url

@patch('modules.music.get_music_client')
def test_music_generation_success(mock_get_client):
    """Test successful music generation prediction."""
    mock_client = MagicMock()
    mock_client.predict.return_value = "/path/to/audio.wav"
    mock_get_client.return_value = mock_client

    path, err = generate_music("happy song")

    assert err is None
    assert path == "/path/to/audio.wav"
    mock_client.predict.assert_called_once_with(
        text_prompt="happy song",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

@patch('modules.video.get_video_client')
def test_video_generation_success(mock_get_client):
    """Test successful video generation prediction."""
    mock_client = MagicMock()
    mock_client.predict.return_value = "/path/to/video.mp4"
    mock_get_client.return_value = mock_client

    path, err = generate_video("running dog")

    assert err is None
    assert path == "/path/to/video.mp4"
    mock_client.predict.assert_called_once_with(
        "running dog",
        -1,
        16,
        25,
        api_name="/generate_video"
    )

def test_keyword_routing():
    """Test the logic for keyword routing used in app.py"""
    IMAGE_KEYWORDS = ['нарисуй', 'фото', 'изображение']
    MUSIC_KEYWORDS = ['музыка', 'песня', 'трек']
    VIDEO_KEYWORDS = ['видео', 'ролик']

    def check_routing(prompt):
        prompt_lower = prompt.lower()
        is_image = any(kw in prompt_lower for kw in IMAGE_KEYWORDS)
        is_music = any(kw in prompt_lower for kw in MUSIC_KEYWORDS)
        is_video = any(kw in prompt_lower for kw in VIDEO_KEYWORDS)
        return is_image, is_music, is_video

    assert check_routing("Нарисуй мне кота") == (True, False, False)
    assert check_routing("Сгенерируй видео про космос") == (False, False, True)
    assert check_routing("Включи веселую песня") == (False, True, False)
    assert check_routing("Просто текст") == (False, False, False)
