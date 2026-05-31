import re

def get_route(prompt: str) -> str:
    """
    Determine the type of generation requested based on Russian keywords in the prompt.
    Returns 'image', 'music', 'video', or 'text' by default.
    """
    prompt_lower = prompt.lower()

    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк']
    music_keywords = ['музык', 'песн', 'песен', 'трек']
    video_keywords = ['видео', 'ролик']

    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'
    elif any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'
    elif any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    return 'text'
