import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Красивое ФОТО пейзажа") == "image"
    assert get_route("Сгенерируй изображение собаки") == "image"
    assert get_route("Покажи картинку машины") == "image"

def test_get_route_music():
    assert get_route("Включи музыку") == "music"
    assert get_route("Создай песню про любовь") == "music"
    assert get_route("Сгенерируй крутой трек") == "music"
    assert get_route("Напиши мне веселую песенку") == "music"

def test_get_route_video():
    assert get_route("Сделай видео с котиками") == "video"
    assert get_route("Сними короткий ролик про город") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи сказку на ночь") == "text"
    assert get_route("Что такое искусственный интеллект?") == "text"

def test_get_route_mixed_keywords():
    # It should match the first condition it hits in the code, which is image > music > video
    assert get_route("Нарисуй фото и сделай видео") == "image"
    assert get_route("Сделай видео и включи музыку") == "music"
