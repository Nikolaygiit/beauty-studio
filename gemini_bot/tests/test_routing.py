import pytest
from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("Нарисуй красивый пейзаж") == "image"
    assert route_prompt("Покажи фото кота") == "image"
    assert route_prompt("Сделай изображение собаки") == "image"
    assert route_prompt("Хочу картинку") == "image"

def test_route_prompt_music():
    assert route_prompt("Включи музыку") == "music"
    assert route_prompt("Сгенерируй песню про любовь") == "music"
    assert route_prompt("Напиши трек") == "music"
    assert route_prompt("Спой песенку") == "music"

def test_route_prompt_video():
    assert route_prompt("Создай видео") == "video"
    assert route_prompt("Сделай ролик про природу") == "video"
    assert route_prompt("Покажи клип") == "video"

def test_route_prompt_text():
    assert route_prompt("Привет, как дела?") == "text"
    assert route_prompt("Расскажи сказку") == "text"
    assert route_prompt("Напиши код на питоне") == "text"

def test_route_prompt_case_insensitivity():
    assert route_prompt("НАРИСУЙ") == "image"
    assert route_prompt("МуЗыКа") == "music"
    assert route_prompt("вИдЕо") == "video"
