import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("хочу фото гор") == "image"
    assert get_route("сгенерируй изображение") == "image"
    assert get_route("покажи картинку") == "image"

def test_get_route_music():
    assert get_route("создай музыку") == "music"
    assert get_route("спой песню") == "music"
    assert get_route("включи песенку") == "music"
    assert get_route("сделай трек") == "music"

def test_get_route_video():
    assert get_route("сделай видео") == "video"
    assert get_route("запиши ролик") == "video"

def test_get_route_text():
    assert get_route("привет, как дела?") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("напиши код на python") == "text"
