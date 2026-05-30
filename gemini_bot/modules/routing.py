def get_route(prompt: str) -> str:
    """
    Определяет тип генерации на основе ключевых слов в запросе.
    Возвращает: 'image', 'music', 'video' или 'text'.
    """
    prompt_lower = prompt.lower()

    # Ключевые слова (корни/основы слов) для определения типа контента
    image_keywords = ['нарису', 'фото', 'изображен', 'картинк']
    music_keywords = ['музык', 'песн', 'трек', 'аудио', 'мелоди']
    video_keywords = ['видео', 'ролик', 'анимаци']

    # Проверка на совпадения
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'

    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'

    if any(keyword in prompt_lower for keyword in music_keywords):
        return 'music'

    # По умолчанию - текстовый ответ
    return 'text'
