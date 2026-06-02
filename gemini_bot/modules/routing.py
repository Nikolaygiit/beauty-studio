def route_prompt(prompt: str) -> str:
    """
    Analyzes the prompt and routes it to the correct generation module based on Russian keywords.
    Returns one of: 'image', 'music', 'video', or 'text'.
    """
    prompt_lower = prompt.lower()

    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк', 'рисунок']
    music_keywords = ['музык', 'песн', 'трек', 'мелоди']
    video_keywords = ['видео', 'ролик', 'анимаци']

    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'
    elif any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'
    elif any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'
    else:
        return 'text'
