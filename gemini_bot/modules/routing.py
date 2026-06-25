import re

IMAGE_PATTERN = re.compile(r'\b(?:нарисуй|фото|изображени[а-я]*|картинк[а-я]*)\b', re.IGNORECASE)
MUSIC_PATTERN = re.compile(r'\b(?:музык[а-я]*|песн[а-я]*|трек[а-я]*)\b', re.IGNORECASE)
VIDEO_PATTERN = re.compile(r'\b(?:видео[а-я]*|ролик[а-я]*)\b', re.IGNORECASE)

def route_prompt(prompt: str) -> str:
    """
    Routes the prompt to 'image', 'music', 'video', or 'text' module based on keywords.
    """
    prompt_lower = prompt.lower()

    if VIDEO_PATTERN.search(prompt_lower):
        return 'video'
    elif MUSIC_PATTERN.search(prompt_lower):
        return 'music'
    elif IMAGE_PATTERN.search(prompt_lower):
        return 'image'
    else:
        return 'text'
