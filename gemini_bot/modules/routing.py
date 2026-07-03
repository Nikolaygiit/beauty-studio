import re

# Route names
ROUTE_IMAGE = 'image'
ROUTE_MUSIC = 'music'
ROUTE_VIDEO = 'video'
ROUTE_TEXT = 'text'

# Regexes for intent detection
# We use \b to match word boundaries and match specific variations or prefixes.

# For image: 'нарисуй', 'фото', 'фотография', 'изображение'
# using explicit alternatives for short words like 'фото' to avoid false positives on 'фотосинтез'
REGEX_IMAGE = re.compile(r'\b(нарисуй[а-я]*|фото|фотографи[яиюей]|изображени[еяюем])\b', re.IGNORECASE)

# For music: 'музык', 'песн', 'трек'
REGEX_MUSIC = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b', re.IGNORECASE)

# For video: 'видео', 'ролик'
REGEX_VIDEO = re.compile(r'\b(видео|ролик[а-я]*)\b', re.IGNORECASE)

def get_route(prompt: str) -> str:
    """
    Determines the routing intent based on keywords in the Russian prompt.
    Checks video, then music, then image, then falls back to text.
    """
    prompt_lower = prompt.lower()

    if REGEX_VIDEO.search(prompt_lower):
        return ROUTE_VIDEO

    if REGEX_MUSIC.search(prompt_lower):
        return ROUTE_MUSIC

    if REGEX_IMAGE.search(prompt_lower):
        return ROUTE_IMAGE

    return ROUTE_TEXT
