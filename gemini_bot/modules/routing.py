import re

def get_media_route(prompt: str) -> str:
    """
    Evaluates the prompt containing Russian keywords to determine if it's requesting
    image, music, or video generation. Returns the route or 'text' by default.
    """
    prompt_lower = prompt.lower()

    # Image keywords: нарисуй, фото, изображение
    image_pattern = re.compile(r'\b(нарисуй|фото|изображение|сгенерируй картинку)\b')
    if image_pattern.search(prompt_lower):
        return 'image'

    # Music keywords: музык, песн, песен, трек
    # We want to match "музыка", "музыку", "песня", "песню", but maybe not "музыкантов"
    # To keep it simple and consistent with instructions: word boundaries on "музык" + some morphological endings
    music_pattern = re.compile(r'\b(музык[уаеи]|песн[яюие]|песен|трек[аиуе]*)\b')
    if music_pattern.search(prompt_lower):
        return 'music'

    # Video keywords: видео, ролик
    video_pattern = re.compile(r'\b(видео|ролик[а-я]*)\b')
    if video_pattern.search(prompt_lower):
        return 'video'

    return 'text'
