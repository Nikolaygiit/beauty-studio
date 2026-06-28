import re

def get_route(prompt: str) -> str:
    """
    Evaluates the prompt based on Russian keywords and returns the route.
    Uses regex with word boundaries and optional suffix matching.
    Routes: 'image', 'music', 'video', 'text'
    """
    prompt_lower = prompt.lower()

    # Image route keywords: нарисуй, фото, изображение
    image_pattern = re.compile(r'\b(?:нарисуй[а-я]*|фото[а-я]*|изображени[а-я]*)\b')
    if image_pattern.search(prompt_lower):
        return 'image'

    # Music route keywords: музык, песн, песен, трек
    music_pattern = re.compile(r'\b(?:музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b')
    if music_pattern.search(prompt_lower):
        return 'music'

    # Video route keywords: видео, ролик
    video_pattern = re.compile(r'\b(?:видео[а-я]*|ролик[а-я]*)\b')
    if video_pattern.search(prompt_lower):
        return 'video'

    return 'text'
