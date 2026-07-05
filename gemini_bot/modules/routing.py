import re

def get_route(prompt: str) -> str:
    """
    Evaluates the prompt for Russian media generation keywords.
    Returns 'image', 'music', 'video', or 'text'.
    """
    prompt = prompt.lower()

    # Image keywords: нарисуй, фото, фотография, изображение
    # Explicit variations for short stems to prevent false positives (like 'фотосинтез')
    image_pattern = re.compile(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*)\b', re.IGNORECASE)

    # Music keywords: музык, песн, песен, трек
    music_pattern = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', re.IGNORECASE)

    # Video keywords: видео, ролик
    video_pattern = re.compile(r'\b(видео|ролик[а-я]*)\b', re.IGNORECASE)

    if image_pattern.search(prompt):
        return 'image'
    elif music_pattern.search(prompt):
        return 'music'
    elif video_pattern.search(prompt):
        return 'video'
    else:
        return 'text'
