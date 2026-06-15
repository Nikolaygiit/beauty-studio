import re

def get_route(prompt: str) -> str:
    """
    Routes the user prompt to the appropriate generation module based on keywords.
    Returns one of: 'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    # Image keywords: нарисуй, фото, изображение, картинка
    if re.search(r'\b(нарисуй|фото|изображени|картинк)', prompt_lower):
        return 'image'

    # Music keywords: музык, песн, песен, трек
    if re.search(r'\b(музык|песн|песен|трек)', prompt_lower):
        return 'music'

    # Video keywords: видео, ролик
    if re.search(r'\b(видео|ролик)', prompt_lower):
        return 'video'

    # Default to text
    return 'text'
