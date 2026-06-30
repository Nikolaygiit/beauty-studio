import re

def get_route(prompt: str) -> str:
    """
    Analyzes the prompt to determine the generation route based on Russian keywords.
    Supported routes: 'image', 'music', 'video', 'text'.
    """
    if not prompt:
        return 'text'

    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = re.compile(r'\b(нарисуй[а-я]*|фото[а-я]*|изображение[а-я]*|картинк[а-я]*)\b')
    if image_keywords.search(prompt_lower):
        return 'image'

    # Music keywords
    music_keywords = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b')
    if music_keywords.search(prompt_lower):
        return 'music'

    # Video keywords
    video_keywords = re.compile(r'\b(видео[а-я]*|ролик[а-я]*)\b')
    if video_keywords.search(prompt_lower):
        return 'video'

    return 'text'
