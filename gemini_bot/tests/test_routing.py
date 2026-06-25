import pytest
from modules.routing import route_prompt

def test_route_prompt_video():
    assert route_prompt("сделай видео с котиком") == "video"
    assert route_prompt("РОЛИК про природу") == "video"

def test_route_prompt_music():
    assert route_prompt("сочини музыку") == "music"
    assert route_prompt("включи песню") == "music"
    assert route_prompt("крутой трек") == "music"

def test_route_prompt_image():
    assert route_prompt("нарисуй дом") == "image"
    assert route_prompt("сделай фото") == "image"
    assert route_prompt("красивое изображение") == "image"
    assert route_prompt("картинка кота") == "image"

def test_route_prompt_text():
    assert route_prompt("расскажи анекдот") == "text"
    assert route_prompt("как дела?") == "text"
    assert route_prompt("напиши код на python") == "text"
