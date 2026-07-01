import pytest
from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Сделай фото леса") == "image"
    assert get_route("красивое изображение гор") == "image"

def test_get_route_music():
    assert get_route("создай музыку для релакса") == "music"
    assert get_route("спой песню о любви") == "music"
    assert get_route("сделай веселый трек") == "music"

def test_get_route_video():
    assert get_route("сделай видео с собакой") == "video"
    assert get_route("смешной ролик про котов") == "video"

def test_get_route_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи сказку") == "text"
    assert get_route("Что такое фотосинтез?") == "text"

def test_get_route_case_insensitive():
    assert get_route("НАРИСУЙ дом") == "image"
    assert get_route("МуЗыКальная пауза") == "music" # 'МуЗыКа' will match 'музык' prefix
