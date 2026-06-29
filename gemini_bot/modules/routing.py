import re

# We will use regex with optional suffixes to match Russian words and their morphological variations
image_keywords = re.compile(r'\b(нарисуй|фото|изображени[а-я]*|картинк[а-я]*)\b', re.IGNORECASE)
music_keywords = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен|трек[а-я]*)\b', re.IGNORECASE)
video_keywords = re.compile(r'\b(видео|ролик[а-я]*)\b', re.IGNORECASE)

def route_prompt(prompt: str) -> str:
    """
    Evaluates the prompt and returns the routing intent.
    Routes: 'image', 'music', 'video', 'text'
    """
    if image_keywords.search(prompt):
        return 'image'
    elif music_keywords.search(prompt):
        return 'music'
    elif video_keywords.search(prompt):
        return 'video'

    return 'text'
