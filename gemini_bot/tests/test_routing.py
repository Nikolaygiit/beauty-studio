import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("сделай фото леса") == "image"
    assert get_route("покажи фотографию машины") == "image"
    assert get_route("создай изображение города") == "image"

def test_get_route_music():
    assert get_route("напиши музыку для сна") == "music"
    assert get_route("сочини веселую песню") == "music"
    assert get_route("включи крутой трек") == "music"

def test_get_route_video():
    assert get_route("сделай видео с собакой") == "video"
    assert get_route("создай короткий ролик") == "video"

def test_get_route_text():
    assert get_route("привет, как дела?") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("какая сегодня погода?") == "text"

def test_get_route_negative_compounds():
    # "фотосинтез" contains "фото" but should not trigger image generation
    assert get_route("что такое фотосинтез?") == "text"
    # "видеокарта" shouldn't trigger video, but our regex \bвидео\b won't match "видеокарта"
    assert get_route("как работает видеокарта") == "text"
