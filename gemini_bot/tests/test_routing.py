import pytest
from gemini_bot.modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй красивого кота") == "image"
    assert get_route("сделай фото заката") == "image"
    assert get_route("покажи изображение машины") == "image"

def test_get_route_music():
    assert get_route("сгенерируй музыку для релакса") == "music"
    assert get_route("включи песню про любовь") == "music"
    assert get_route("сделай трек в стиле рок") == "music"

def test_get_route_video():
    assert get_route("создай видео с летящей птицей") == "video"
    assert get_route("сделай короткий ролик") == "video"
    assert get_route("анимация прыгающего мяча") == "video"

def test_get_route_text():
    assert get_route("привет, как дела?") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("напиши код на python") == "text"
