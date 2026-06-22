import pytest
from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("покажи фото собаки") == "image"
    assert route_prompt("сделай красивое изображение") == "image"
    assert route_prompt("сделай картинку") == "image"

def test_route_prompt_music():
    assert route_prompt("сгенерируй музыку") == "music"
    assert route_prompt("напиши песню") == "music"
    assert route_prompt("крутой трек") == "music"

def test_route_prompt_video():
    assert route_prompt("сделай видео про космос") == "video"
    assert route_prompt("сними ролик") == "video"

def test_route_prompt_text():
    assert route_prompt("привет, как дела?") == "text"
    assert route_prompt("расскажи сказку") == "text"
    assert route_prompt("что такое фотосинтез") == "text" # "фото" in "фотосинтез" should not match

def test_route_prompt_mixed():
    # If multiple keywords present, image takes precedence based on the order in route_prompt
    assert route_prompt("нарисуй видео") == "image"
    assert route_prompt("музыку к видео") == "music"
