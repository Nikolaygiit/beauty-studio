import re

def get_route(prompt: str) -> str:
    prompt_lower = prompt.lower()

    # Image routing
    # Keywords: нарисуй, фото, изображение, картинка, сгенерируй фото
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображени', 'картинк']):
        return 'image'

    # Music routing
    # Keywords: музык, песн, песен, трек, мелоди
    if any(keyword in prompt_lower for keyword in ['музык', 'песн', 'песен', 'трек', 'мелоди']):
        return 'music'

    # Video routing
    # Keywords: видео, ролик
    if any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        return 'video'

    # Default to text
    return 'text'
