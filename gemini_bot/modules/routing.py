import re

def get_route(prompt: str) -> str:
    """
    Routes the generation intent based on Russian keywords with morphological handling.
    Returns one of: 'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    # Image routing
    if re.search(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*)\b', prompt_lower):
        return 'image'

    # Music routing
    if re.search(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', prompt_lower):
        return 'music'

    # Video routing
    if re.search(r'\b(видео|ролик)\b', prompt_lower):
        return 'video'

    # Default to text
    return 'text'
