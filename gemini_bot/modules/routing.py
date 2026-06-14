def get_route(prompt: str) -> str:
    """Routes the prompt to the appropriate generation module based on keywords."""
    prompt_lower = prompt.lower()

    image_keywords = ['нарисуй', 'фото', 'изображение']
    music_keywords = ['музык', 'песн', 'песен', 'трек']
    video_keywords = ['видео', 'ролик']

    for kw in image_keywords:
        if kw in prompt_lower:
            return 'image'

    for kw in music_keywords:
        if kw in prompt_lower:
            return 'music'

    for kw in video_keywords:
        if kw in prompt_lower:
            return 'video'

    return 'text'
