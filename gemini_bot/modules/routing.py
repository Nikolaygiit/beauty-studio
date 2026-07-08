import re

def route_prompt(prompt: str) -> str:
    """
    Analyzes the prompt to determine the requested media type.
    Returns 'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    # Check for image triggers
    image_pattern = re.compile(r'\b(нарисуй[а-я]*|фото|фотографи[а-я]*|изображени[а-я]*)\b')
    if image_pattern.search(prompt_lower):
        return 'image'

    # Check for music triggers
    music_pattern = re.compile(r'\b(музык[а-я]*|песн[а-я]*|песен[а-я]*|трек[а-я]*)\b')
    if music_pattern.search(prompt_lower):
        return 'music'

    # Check for video triggers
    video_pattern = re.compile(r'\b(видео|ролик[а-я]*)\b')
    if video_pattern.search(prompt_lower):
        return 'video'

    # Default to text
    return 'text'
