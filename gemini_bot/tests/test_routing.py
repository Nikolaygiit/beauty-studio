import pytest

# Simulate the morphology logic from app.py
def route_prompt(prompt):
    prompt_lower = prompt.lower()

    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        return "image"
    elif any(keyword in prompt_lower for keyword in ["музык", "песн", "трек"]):
        return "music"
    elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        return "video"
    else:
        return "text"

def test_image_routing():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("покажи фото собаки") == "image"
    assert route_prompt("сгенерируй изображение города") == "image"
    assert route_prompt("НАРИСУЙ дом") == "image"

def test_music_routing():
    assert route_prompt("включи музыку") == "music"
    assert route_prompt("напиши песню") == "music"
    assert route_prompt("создай новый трек") == "music"
    assert route_prompt("классная музыка") == "music"
    assert route_prompt("спой песню") == "music"

def test_video_routing():
    assert route_prompt("сделай видео") == "video"
    assert route_prompt("покажи короткий ролик") == "video"
    assert route_prompt("ВИДЕО с котиками") == "video"

def test_text_routing():
    assert route_prompt("привет, как дела?") == "text"
    assert route_prompt("напиши код на python") == "text"
    assert route_prompt("расскажи сказку") == "text"
    assert route_prompt("какая погода?") == "text"
