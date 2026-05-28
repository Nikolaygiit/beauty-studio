def get_routing(prompt: str):
    prompt_lower = prompt.lower()
    if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
        return "image"
    elif any(keyword in prompt_lower for keyword in ['музык', 'песн', 'песен', 'трек']):
        return "music"
    elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
        return "video"
    else:
        return "text"
