def route_prompt(prompt: str) -> str:
    """
    Analyzes the Russian prompt and returns the correct module route:
    'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    # Check for image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    # Check for music keywords
    music_keywords = ['музык', 'песн', 'трек', 'мелоди']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # Check for video keywords
    video_keywords = ['видео', 'ролик', 'клип']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    # Default to text
    return 'text'
