def get_route(prompt: str) -> str:
    """
    Evaluates the prompt for specific Russian keywords and routes
    the request to the appropriate module. Accounts for word morphology
    by checking for common roots.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображени', 'картинк']
    for keyword in image_keywords:
        if keyword in prompt_lower:
            return 'image'

    # Music keywords
    music_keywords = ['музык', 'песн', 'трек', 'мелоди']
    for keyword in music_keywords:
        if keyword in prompt_lower:
            return 'music'

    # Video keywords
    video_keywords = ['видео', 'ролик']
    for keyword in video_keywords:
        if keyword in prompt_lower:
            return 'video'

    # Default to text
    return 'text'
