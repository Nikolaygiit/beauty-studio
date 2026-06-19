import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй кота") == "image"
    assert get_route("Сделай фото леса") == "image"
    assert get_route("Красивое ИЗОБРАЖЕНИЕ") == "image"

def test_get_route_music():
    assert get_route("Напиши музыку для сна") == "music"
    assert get_route("Спой песню") == "music"
    assert get_route("Крутой ТРЕК") == "music"

def test_get_route_video():
    assert get_route("Сними видео") == "video"
    assert get_route("Смешной РОЛИК") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Что такое квантовая физика?") == "text"
