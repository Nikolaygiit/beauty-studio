def determine_route(prompt: str) -> str:
    """
    Evaluates the prompt containing Russian keywords to determine the media route.
    Returns: 'image', 'video', 'music', or 'text'
    """
    prompt_lower = prompt.lower()

    # Image routing
    if any(word in prompt_lower for word in ['нарисуй', 'фото', 'изображение', 'картинк']):
        return 'image'

    # Music routing
    if any(word in prompt_lower for word in ['музык', 'песн', 'песен', 'трек']):
        return 'music'

    # Video routing
    if any(word in prompt_lower for word in ['видео', 'ролик']):
        return 'video'

    # Default
    return 'text'
