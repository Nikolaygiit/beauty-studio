def get_route(prompt: str) -> str:
    """
    Evaluates the prompt and returns the correct module route based on Russian keywords.
    """
    prompt_lower = prompt.lower()

    # Image keywords
    if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
        return "image"

    # Music keywords
    if any(keyword in prompt_lower for keyword in ["музык", "песн", "песен", "трек"]):
        return "music"

    # Video keywords
    if any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
        return "video"

    # Default to text
    return "text"
