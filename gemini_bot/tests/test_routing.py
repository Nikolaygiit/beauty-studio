import pytest
from modules.routing import get_routing

def test_routing_image():
    assert get_routing("Нарисуй мне кота") == "image"
    assert get_routing("Сделай фото леса") == "image"
    assert get_routing("Сгенерируй изображение собаки") == "image"

def test_routing_music():
    assert get_routing("Включи музыку") == "music"
    assert get_routing("Сыграй песню") == "music"
    assert get_routing("Спой песенку") == "music"
    assert get_routing("Сделай крутой трек") == "music"

def test_routing_video():
    assert get_routing("Сделай видео") == "video"
    assert get_routing("Сними ролик") == "video"

def test_routing_text():
    assert get_routing("Привет, как дела?") == "text"
    assert get_routing("Что такое космос?") == "text"
    assert get_routing("Расскажи стих") == "text"
