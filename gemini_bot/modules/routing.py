import re

def route_prompt(prompt: str) -> str:
    """Routes the prompt to the appropriate module based on Russian keywords."""
    prompt_lower = prompt.lower()

    # Use word boundaries (\b) but allow for Russian prefixes/suffixes somewhat loosely,
    # or match the stems directly using word boundaries

    image_pattern = re.compile(r'\b(нарисуй|фото|изображени[ея]|картинк[аи]|сгенерируй изображение)\b')
    music_pattern = re.compile(r'\b(музык[уа]|песн[юи]|песен|трек|мелоди[юи])\b')
    video_pattern = re.compile(r'\b(видео|ролик|сгенерируй видео)\b')

    if image_pattern.search(prompt_lower):
        return "image"
    elif music_pattern.search(prompt_lower):
        return "music"
    elif video_pattern.search(prompt_lower):
        return "video"
    else:
        return "text"
