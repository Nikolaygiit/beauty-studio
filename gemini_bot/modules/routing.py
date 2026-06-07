def determine_route(prompt: str) -> str:
    """
    Determines the appropriate generation route based on keywords in the prompt.
    Returns: 'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    # Music keywords
    music_keywords = ['музык', 'песн', 'трек', 'аудио', 'мелоди']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # Video keywords
    video_keywords = ['видео', 'ролик', 'анимаци']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    # Default to text
    return 'text'
