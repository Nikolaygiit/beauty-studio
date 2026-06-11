import pytest
from modules.routing import determine_route

def test_determine_route_image():
    assert determine_route("Нарисуй мне кота") == "image"
    assert determine_route("Покажи фото природы") == "image"
    assert determine_route("Сделай изображение собаки") == "image"
    assert determine_route("крутая картинка машины") == "image"

def test_determine_route_music():
    assert determine_route("Включи музыку") == "music"
    assert determine_route("напиши песню про любовь") == "music"
    assert determine_route("спой песенку") == "music"
    assert determine_route("включи крутой трек") == "music"

def test_determine_route_video():
    assert determine_route("Сделай смешное видео") == "video"
    assert determine_route("покажи короткий ролик") == "video"

def test_determine_route_text():
    assert determine_route("Привет, как дела?") == "text"
    assert determine_route("Что такое искусственный интеллект?") == "text"
    assert determine_route("Напиши код на python") == "text"

def test_determine_route_case_insensitivity():
    assert determine_route("НАРИСУЙ") == "image"
    assert determine_route("МУЗЫКА") == "music"
    assert determine_route("ВИДЕО") == "video"
