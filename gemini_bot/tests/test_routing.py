import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Сделай фото леса") == "image"
    assert get_route("Создай изображение машины") == "image"
    assert get_route("Покажи картинку") == "image"

def test_get_route_music():
    assert get_route("Сгенерируй музыку") == "music"
    assert get_route("Напиши песню") == "music"
    assert get_route("Включи трек") == "music"

def test_get_route_video():
    assert get_route("Создай видео") == "video"
    assert get_route("Сделай ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи сказку") == "text"
    assert get_route("Что такое нейросеть?") == "text"

def test_get_route_case_insensitive():
    assert get_route("НАРИСУЙ собаку") == "image"
    assert get_route("МУЗЫКа громче") == "music"
    assert get_route("ВИДЕО про космос") == "video"
