import pytest
from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("покажи фото собаки") == "image"
    assert route_prompt("изображение города") == "image"
    assert route_prompt("Сгенерируй изображение") == "image"

def test_route_prompt_music():
    assert route_prompt("создай музыку") == "music"
    assert route_prompt("музыка для сна") == "music"
    assert route_prompt("напиши песню") == "music"
    assert route_prompt("спой песню") == "music"
    assert route_prompt("веселый трек") == "music"

def test_route_prompt_video():
    assert route_prompt("сделай видео") == "video"
    assert route_prompt("покажи ролик") == "video"

def test_route_prompt_text():
    assert route_prompt("привет, как дела?") == "text"
    assert route_prompt("расскажи сказку") == "text"
    assert route_prompt("") == "text"
