import re

def get_route(prompt: str) -> str:
    """
    Routes the user prompt to the appropriate generation module based on keywords.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    # Using \b for word boundaries. "фото" should be explicit, but "фотографи" can have suffixes like "фотографию"
    image_pattern = re.compile(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*|картинк[а-я]*)\b', re.IGNORECASE)
    if image_pattern.search(prompt_lower):
        return 'image'

    # Music keywords
    music_pattern = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', re.IGNORECASE)
    if music_pattern.search(prompt_lower):
        return 'music'

    # Video keywords
    video_pattern = re.compile(r'\b(видео|ролик[а-я]*)\b', re.IGNORECASE)
    if video_pattern.search(prompt_lower):
        return 'video'

    # Default to text
    return 'text'
