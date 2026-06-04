import pytest
from gemini_bot.modules.routing import get_route

def test_image_routing():
    assert get_route("Нарисуй красивого кота") == "image"
    assert get_route("Сделай мне фото заката") == "image"
    assert get_route("Сгенерируй картинку с собакой") == "image"

def test_music_routing():
    assert get_route("Напиши песню про любовь") == "music"
    assert get_route("Включи крутой трек") == "music"
    assert get_route("Создай веселую мелодию") == "music"

def test_video_routing():
    assert get_route("Сделай видео с машиной") == "video"
    assert get_route("Короткий ролик") == "video"
    assert get_route("Классная анимация") == "video"

def test_text_routing():
    assert get_route("Как дела?") == "text"
    assert get_route("Напиши код на питоне") == "text"
    assert get_route("Что такое нейросеть?") == "text"
