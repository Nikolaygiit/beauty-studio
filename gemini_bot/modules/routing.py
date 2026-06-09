def get_route(prompt: str) -> str:
    """
    Evaluates the prompt and returns the routing path: 'image', 'music', 'video', or 'text'.
    Uses basic substring matching for Russian keywords.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк', 'рисунок', 'нарисова']
    for kw in image_keywords:
        if kw in prompt_lower:
            return "image"

    # Music keywords
    music_keywords = ['музык', 'песн', 'трек', 'мелоди', 'аудио', 'песен']
    for kw in music_keywords:
        if kw in prompt_lower:
            return "music"

    # Video keywords
    video_keywords = ['видео', 'ролик', 'анимаци']
    for kw in video_keywords:
        if kw in prompt_lower:
            return "video"

    # Default to text
    return "text"
