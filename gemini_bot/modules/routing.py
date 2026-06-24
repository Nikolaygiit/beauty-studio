import re

def get_route(prompt: str) -> str:
    """
    Routes the prompt based on specific Russian keywords to the appropriate module.
    """
    prompt_lower = prompt.lower()

    # Image routing
    image_pattern = re.compile(r'\b(нарисуй[а-я]*|фото[а-я]*|изображени[а-я]*|картинк[а-я]*)\b')
    if image_pattern.search(prompt_lower):
        return 'image'

    # Music routing
    music_pattern = re.compile(r'\b(музык[а-я]*|песн[а-я]*|трек[а-я]*)\b')
    if music_pattern.search(prompt_lower):
        return 'music'

    # Video routing
    video_pattern = re.compile(r'\b(видео[а-я]*|ролик[а-я]*)\b')
    if video_pattern.search(prompt_lower):
        return 'video'

    return 'text'
