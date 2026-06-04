def get_route(prompt):
    prompt_lower = prompt.lower()

    image_keywords = ['нарисуй', 'фото', 'изображение', 'сгенерируй картинку', 'картинка']
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    music_keywords = ['музык', 'песн', 'песен', 'трек', 'мелоди']
    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    video_keywords = ['видео', 'ролик', 'анимаци']
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    return 'text'
