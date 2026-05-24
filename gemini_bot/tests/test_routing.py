import pytest
from app import determine_routing

def test_routing_image():
    assert determine_routing("Нарисуй мне кота") == "image"
    assert determine_routing("Покажи фото заката") == "image"
    assert determine_routing("Сгенерируй изображение") == "image"

def test_routing_music():
    assert determine_routing("Сделай музыку") == "music"
    assert determine_routing("Включи песню") == "music"
    assert determine_routing("Напиши крутой трек") == "music"
    assert determine_routing("Спой песню") == "music"

def test_routing_video():
    assert determine_routing("Сделай видео") == "video"
    assert determine_routing("Короткий ролик") == "video"

def test_routing_text():
    assert determine_routing("Привет, как дела?") == "text"
    assert determine_routing("Расскажи сказку") == "text"
    assert determine_routing("Напиши код на python") == "text"

def test_routing_case_insensitivity():
    assert determine_routing("НАРИСУЙ") == "image"
    assert determine_routing("МуЗыК") == "music"
    assert determine_routing("ВиДеО") == "video"
