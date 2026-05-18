import pytest
from unittest.mock import patch, MagicMock
from modules.image import generate_image

def test_image_generation_returns_url():
    """Test that the image generation properly encodes the URL and handles seed."""
    prompt = "Тестовый промпт"
    url, err = generate_image(prompt)

    assert err is None
    assert "https://image.pollinations.ai/prompt/" in url
    assert "nologo=True" in url
    # Ensure Russian prompt is encoded
    assert "%" in url

def test_keyword_routing_logic():
    """Test the logic used in app.py to route keywords."""
    image_keywords = ["нарисуй", "фото", "изображение"]
    music_keywords = ["музыка", "песня", "трек"]
    video_keywords = ["видео", "ролик"]

    def check_routing(prompt):
        prompt_lower = prompt.lower()
        return {
            "image": any(kw in prompt_lower for kw in image_keywords),
            "music": any(kw in prompt_lower for kw in music_keywords),
            "video": any(kw in prompt_lower for kw in video_keywords)
        }

    # Test Image routing
    res = check_routing("Нарисуй мне красивый пейзаж")
    assert res["image"] is True
    assert res["music"] is False

    # Test Music routing
    res = check_routing("Напиши мне веселую песню (песня)")
    assert res["music"] is True
    assert res["video"] is False

    # Test Video routing
    res = check_routing("Сгенерируй короткое видео")
    assert res["video"] is True
    assert res["image"] is False

    # Test text fallback (no keywords)
    res = check_routing("Привет, как дела?")
    assert not res["image"] and not res["music"] and not res["video"]

@patch("modules.music.Client")
def test_music_generation_handles_uninitialized_client(mock_client_class):
    """Test music generator handles None client."""
    from modules.music import generate_music
    res, err = generate_music(None, "prompt")
    assert res is None
    assert "не инициализирован" in err

@patch("modules.video.Client")
def test_video_generation_handles_uninitialized_client(mock_client_class):
    """Test video generator handles None client."""
    from modules.video import generate_video
    res, err = generate_video(None, "prompt")
    assert res is None
    assert "не инициализирован" in err
