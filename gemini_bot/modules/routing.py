import re

# Regex to match image generation keywords
IMAGE_REGEX = re.compile(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*)\b', re.IGNORECASE)

# Regex to match music generation keywords (with optional suffix match where applicable, avoiding on short stems like фото)
MUSIC_REGEX = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', re.IGNORECASE)

# Regex to match video generation keywords
VIDEO_REGEX = re.compile(r'\b(видео|ролик[а-я]*)\b', re.IGNORECASE)

def get_route(prompt: str) -> str:
    """
    Evaluates the prompt containing Russian keywords and returns the correct module route.
    Returns 'image', 'music', 'video', or 'text'.
    """
    if IMAGE_REGEX.search(prompt):
        return 'image'
    elif MUSIC_REGEX.search(prompt):
        return 'music'
    elif VIDEO_REGEX.search(prompt):
        return 'video'
    return 'text'
