def get_route(prompt: str) -> str:
    """
    Returns the routing destination for a given prompt based on keywords.
    Routes available: "image", "music", "video", "text" (default).
    """
    prompt_lower = prompt.lower()

    # Image keywords
    # Make sure we don't accidentally match "фото" inside words like "фотосинтез"
    import re
    image_pattern = re.compile(r'\b(нарисуй\w*|фото|фотк\w*|изображен\w*|сгенерируй картинку)\b', re.IGNORECASE)
    if image_pattern.search(prompt_lower):
        return "image"

    # Music keywords - checking morphology for 'музык', 'песн', 'трек'
    music_keywords = ["музык", "песн", "песен", "трек"]
    if any(keyword in prompt_lower for keyword in music_keywords):
        return "music"

    # Video keywords
    video_keywords = ["видео", "ролик"]
    if any(keyword in prompt_lower for keyword in video_keywords):
        return "video"

    # Default is text
    return "text"
