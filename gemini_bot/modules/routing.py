import re

def get_route(prompt: str) -> str:
    """
    Determines the appropriate module to route the prompt to based on Russian keywords.
    Keywords:
        - Image: нарисуй, фото, фотография, изображение
        - Music: музык, песн, песен, трек
        - Video: видео, ролик
    Returns one of: 'image', 'music', 'video', 'text'
    """
    prompt_lower = prompt.lower()

    # Use regular expressions to match keywords and their word morphology (optional suffixes)
    # \b ensures word boundaries
    if re.search(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*)\b', prompt_lower):
        return 'image'

    if re.search(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', prompt_lower):
        return 'music'

    if re.search(r'\b(видео[а-я]*|ролик[а-я]*)\b', prompt_lower):
        return 'video'

    return 'text'
