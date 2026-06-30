import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй кота") == "image"
    assert get_route("Покажи фото заката") == "image"
    assert get_route("Сделай изображение") == "image"
    assert get_route("Картинка природы") == "image"

def test_get_route_music():
    assert get_route("Создай музыку") == "music"
    assert get_route("Напиши песню") == "music"
    assert get_route("Сделай трек") == "music"
    assert get_route("Спой песенку") == "music"

def test_get_route_video():
    assert get_route("Сделай видео") == "video"
    assert get_route("Сними ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи стих") == "text"
    assert get_route("Что такое нейросеть?") == "text"
    assert get_route("") == "text"
    assert get_route(None) == "text"
