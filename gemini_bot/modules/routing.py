def get_route(prompt: str) -> str:
    """Определяет тип маршрута на основе ключевых слов в запросе пользователя."""
    lower_prompt = prompt.lower()

    # Ключевые слова для разных модулей
    image_keywords = ['нарисуй', 'фото', 'изображение', 'картинк', 'рисунок']
    music_keywords = ['музык', 'песн', 'трек', 'мелоди']
    video_keywords = ['видео', 'ролик', 'клип']

    # Проверка маршрута видео
    for kw in video_keywords:
        if kw in lower_prompt:
            return "video"

    # Проверка маршрута музыки
    for kw in music_keywords:
        if kw in lower_prompt:
            return "music"

    # Проверка маршрута изображений
    for kw in image_keywords:
        if kw in lower_prompt:
            return "image"

    # По умолчанию - текстовый маршрут
    return "text"
