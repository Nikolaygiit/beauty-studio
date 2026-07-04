import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Сделай фото леса") == "image"
    assert get_route("Сделай фотографию") == "image"
    assert get_route("Генерируй изображение собаки") == "image"
    assert get_route("Покажи картинку") == "image"

def test_get_route_music():
    assert get_route("Включи музыку") == "music"
    assert get_route("Спой песню") == "music"
    assert get_route("Крутой трек") == "music"
    assert get_route("Новая песенка") == "music"

def test_get_route_video():
    assert get_route("Сними видео") == "video"
    assert get_route("Покажи ролик") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи о фотосинтезе") == "text" # "фото" in text shouldn't trigger if boundaries are correct. Actually "фотосинтезе" is a compound word. Wait, regex matches \bфото\b, so "фотосинтезе" won't match "фото". Let's verify this in the test.
