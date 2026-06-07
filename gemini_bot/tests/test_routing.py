import pytest
from modules.routing import determine_route

def test_determine_route_image():
    assert determine_route("Нарисуй мне кота") == "image"
    assert determine_route("красивое фото пейзажа") == "image"
    assert determine_route("сгенерируй изображение собаки") == "image"
    assert determine_route("покажи картинку") == "image"

def test_determine_route_music():
    assert determine_route("создай музыку для сна") == "music"
    assert determine_route("напиши песню о любви") == "music"
    assert determine_route("крутой трек") == "music"
    assert determine_route("аудио фон") == "music"
    assert determine_route("веселая мелодия") == "music"

def test_determine_route_video():
    assert determine_route("сделай видео с машиной") == "video"
    assert determine_route("смешной ролик") == "video"
    assert determine_route("3d анимация") == "video"

def test_determine_route_text():
    assert determine_route("Привет, как дела?") == "text"
    assert determine_route("расскажи сказку") == "text"
    assert determine_route("что такое искусственный интеллект") == "text"
