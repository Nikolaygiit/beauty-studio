import re

def route_prompt(prompt: str) -> str:
    """
    Routes the prompt to the appropriate generation module based on keywords.
    Keywords are matched using regex with word boundaries to prevent false positives.
    """
    prompt_lower = prompt.lower()

    # Check for image keywords
    if re.search(r'\b(нарисуй|фото|изображение|изображения|картинку|картинки)\b', prompt_lower):
        return 'image'

    # Check for music keywords
    if re.search(r'\b(музыка|музыку|музыки|песня|песню|песни|трек|треки)\b', prompt_lower):
        return 'music'

    # Check for video keywords
    if re.search(r'\b(видео|ролик|ролики)\b', prompt_lower):
        return 'video'

    # Default to text generation
    return 'text'
