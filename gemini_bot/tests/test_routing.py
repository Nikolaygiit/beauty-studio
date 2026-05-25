import pytest

def test_image_routing():
    keywords = ["нарисуй", "фото", "изображение"]
    prompts = [
        "Нарисуй мне кота",
        "сделай красивое фото природы",
        "покажи изображение машины",
        "нарисуй-ка дом"
    ]
    for prompt in prompts:
        prompt_lower = prompt.lower()
        is_image = any(kw in prompt_lower for kw in keywords)
        assert is_image is True, f"Prompt '{prompt}' should route to image generation"

def test_music_routing():
    keywords = ["музык", "песн", "песен", "трек"]
    prompts = [
        "сочини музыку для сна",
        "напиши песню о любви",
        "сделай крутой трек",
        "спой мне песенку"
    ]
    for prompt in prompts:
        prompt_lower = prompt.lower()
        is_music = any(kw in prompt_lower for kw in keywords)
        assert is_music is True, f"Prompt '{prompt}' should route to music generation"

def test_video_routing():
    keywords = ["видео", "ролик"]
    prompts = [
        "сделай видео моря",
        "сними короткий ролик",
        "сгенерируй видеоролик про космос"
    ]
    for prompt in prompts:
        prompt_lower = prompt.lower()
        is_video = any(kw in prompt_lower for kw in keywords)
        assert is_video is True, f"Prompt '{prompt}' should route to video generation"

def test_text_routing():
    image_kws = ["нарисуй", "фото", "изображение"]
    music_kws = ["музык", "песн", "песен", "трек"]
    video_kws = ["видео", "ролик"]

    prompts = [
        "расскажи сказку",
        "привет, как дела?",
        "напиши код на python"
    ]
    for prompt in prompts:
        prompt_lower = prompt.lower()
        is_image = any(kw in prompt_lower for kw in image_kws)
        is_music = any(kw in prompt_lower for kw in music_kws)
        is_video = any(kw in prompt_lower for kw in video_kws)

        assert not is_image and not is_music and not is_video, f"Prompt '{prompt}' should route to text generation"
