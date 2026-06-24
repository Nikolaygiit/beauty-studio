import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Фотография природы") == "image"
    assert get_route("Красивое изображение") == "image"

def test_get_route_music():
    assert get_route("Сделай мне музыку") == "music"
    assert get_route("Веселая песня") == "music"
    assert get_route("Новый трек") == "music"

def test_get_route_video():
    assert get_route("Смешное видео") == "video"
    assert get_route("Короткий ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Напиши код на питоне") == "text"
