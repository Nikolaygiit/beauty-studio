import re

def route_prompt(prompt: str) -> str:
    """
    Определяет маршрут запроса на основе ключевых слов в тексте.
    Возвращает 'image', 'music', 'video' или 'text' по умолчанию.
    Учитывает русскую морфологию корней слов.
    """
    prompt_lower = prompt.lower()

    # Регулярные выражения для поиска корней и слов-триггеров
    image_pattern = r'(нарисуй|фото|изображени|изобрази|картинк)'
    music_pattern = r'(музык|песн|трек|мелоди)'
    video_pattern = r'(видео|ролик|клип)'

    if re.search(image_pattern, prompt_lower):
        return 'image'
    elif re.search(music_pattern, prompt_lower):
        return 'music'
    elif re.search(video_pattern, prompt_lower):
        return 'video'
    else:
        return 'text'
