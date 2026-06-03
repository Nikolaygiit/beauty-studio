def get_route(prompt: str) -> str:
    """
    Routes the prompt to the appropriate generation module based on keywords.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    # Music keywords
    music_keywords = ['музык', 'песн', 'песен', 'трек']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # Video keywords
    video_keywords = ['видео', 'ролик']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    # Default is text
    return 'text'
