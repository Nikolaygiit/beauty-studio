import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй красивый пейзаж") == "image"
    assert get_route("Сделай фото кота") == "image"
    assert get_route("Создай изображение собаки") == "image"
    assert get_route("Покажи картинку машины") == "image"

def test_get_route_music():
    assert get_route("Напиши классную музыку") == "music"
    assert get_route("Включи песню про любовь") == "music"
    assert get_route("Создай крутой трек") == "music"
    assert get_route("Сгенерируй мелодию") == "music"

def test_get_route_video():
    assert get_route("Сделай смешное видео") == "video"
    assert get_route("Покажи ролик про природу") == "video"

def test_get_route_text():
    assert get_route("Расскажи сказку") == "text"
    assert get_route("Какая сегодня погода?") == "text"
    assert get_route("Привет, как дела?") == "text"
