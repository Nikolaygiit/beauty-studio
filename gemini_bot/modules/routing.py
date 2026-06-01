def get_route(prompt: str) -> str:
    """
    Evaluates the prompt containing Russian keywords and returns the route.
    Available routes: 'image', 'music', 'video', 'text'
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    # Music keywords
    music_keywords = ['музык', 'песн', 'трек']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # Video keywords
    video_keywords = ['видео', 'ролик']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    # Default route
    return 'text'
