import re

def get_route(prompt: str) -> str:
    """
    Routes the user prompt to the correct media module based on Russian keywords.
    Returns 'image', 'music', 'video', or 'text' by default.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_pattern = re.compile(r'\b(нарисуй[а-я]*|фото[а-я]*|изображени[а-я]*|картинк[а-я]*)\b')
    if image_pattern.search(prompt_lower):
        return 'image'

    # Music keywords
    music_pattern = re.compile(r'\b(музык[а-я]*|песн[а-я]*|трек[а-я]*)\b')
    if music_pattern.search(prompt_lower):
        return 'music'

    # Video keywords
    video_pattern = re.compile(r'\b(видео[а-я]*|ролик[а-я]*)\b')
    if video_pattern.search(prompt_lower):
        return 'video'

    return 'text'
