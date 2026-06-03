from gemini_bot.modules.routing import get_route
from gemini_bot.modules.image import generate_image
import urllib.parse

def test_routing_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Покажи фото заката") == "image"
    assert get_route("красивое изображение города") == "image"
    assert get_route("сделай картинку") == "image"

def test_routing_music():
    assert get_route("Напиши мне музыку") == "music"
    assert get_route("спой песню") == "music"
    assert get_route("включи крутой трек") == "music"
    assert get_route("хочу много песен") == "music"

def test_routing_video():
    assert get_route("Сделай видео") == "video"
    assert get_route("сними ролик") == "video"

def test_routing_text():
    assert get_route("Как дела?") == "text"
    assert get_route("Напиши код на питоне") == "text"

def test_image_url_generation():
    prompt = "Кот в космосе"
    url, error = generate_image(prompt)
    assert error is None
    assert url is not None
    assert "https://image.pollinations.ai/prompt/" in url

    encoded_prompt = urllib.parse.quote(prompt)
    assert encoded_prompt in url
    assert "?seed=" in url
