import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Красивое фото природы") == "image"
    assert get_route("Сгенерируй изображение собаки") == "image"

def test_get_route_music():
    assert get_route("Сделай музыку") == "music"
    assert get_route("Спой песню") == "music"
    assert get_route("Напиши трек для тренировки") == "music"

def test_get_route_video():
    assert get_route("Сделай видео") == "video"
    assert get_route("Сними ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Что такое нейросеть?") == "text"

def test_get_route_case_insensitivity():
    assert get_route("НАРИСУЙ") == "image"
    assert get_route("МУЗЫКА") == "music"
    assert get_route("ВИДЕО") == "video"
