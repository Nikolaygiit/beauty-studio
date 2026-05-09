import pytest
import sys
import os

# Add the gemini_bot directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import determine_media_type
from modules.image import generate_image

def test_determine_media_type_image():
    assert determine_media_type("Нарисуй мне красивый пейзаж") == "image"
    assert determine_media_type("Сделай фото кота") == "image"
    assert determine_media_type("Покажи изображение машины") == "image"

def test_determine_media_type_music():
    assert determine_media_type("Сделай мне музыка") == "music"
    assert determine_media_type("Создай трек про лето") == "music"
    assert determine_media_type("Напиши песня о любви") == "music"

def test_determine_media_type_video():
    assert determine_media_type("Создай крутое видео") == "video"
    assert determine_media_type("Сними ролик про собаку") == "video"

def test_determine_media_type_text():
    assert determine_media_type("Привет, как дела?") == "text"
    assert determine_media_type("Что такое искусственный интеллект?") == "text"

def test_generate_image_url():
    url, error = generate_image("test prompt")
    assert url is not None
    assert error is None
    assert "https://image.pollinations.ai/prompt/test%20prompt" in url
    assert "?seed=" in url
