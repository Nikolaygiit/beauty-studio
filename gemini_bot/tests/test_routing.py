import pytest
from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("покажи фото машины") == "image"
    assert route_prompt("красивое изображение леса") == "image"
    assert route_prompt("картинка собаки") == "image"

def test_route_prompt_music():
    assert route_prompt("сгенерируй музыку для отдыха") == "music"
    assert route_prompt("напиши песню про любовь") == "music"
    assert route_prompt("включи крутой трек") == "music"

def test_route_prompt_video():
    assert route_prompt("сделай видео с котиками") == "video"
    assert route_prompt("короткий ролик про город") == "video"
    assert route_prompt("крутая анимация") == "video"

def test_route_prompt_text():
    assert route_prompt("привет, как дела?") == "text"
    assert route_prompt("расскажи сказку") == "text"
    assert route_prompt("сколько будет 2+2?") == "text"

def test_route_prompt_case_insensitivity():
    assert route_prompt("НАРИСУЙ ДОМ") == "image"
    assert route_prompt("ПеСнЯ про лето") == "music"
    assert route_prompt("ВИДЕО с собакой") == "video"
