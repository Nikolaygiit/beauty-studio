def route_prompt(prompt: str) -> str:
    """
    Evaluates the prompt to determine the correct module route based on Russian keywords.
    Returns: 'image', 'music', 'video', or 'text'.
    """
    if not prompt:
        return 'text'

    prompt_lower = prompt.lower()

    # Image keywords
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинку', 'картинка', 'сгенерируй изображение']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    # Music keywords
    music_keywords = ['музык', 'песн', 'трек', 'мелодию']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # Video keywords
    video_keywords = ['видео', 'ролик']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    return 'text'
