import pytest
from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("покажи фото собаки") == "image"
    assert route_prompt("красивое изображение природы") == "image"

def test_route_prompt_music():
    assert route_prompt("напиши музыку для сна") == "music"
    assert route_prompt("веселая песня") == "music"
    assert route_prompt("крутой трек") == "music"

def test_route_prompt_video():
    assert route_prompt("создай видео с закатом") == "video"
    assert route_prompt("смешной ролик") == "video"

def test_route_prompt_text():
    assert route_prompt("как дела?") == "text"
    assert route_prompt("расскажи сказку") == "text"
    assert route_prompt("что такое гравитация") == "text"
