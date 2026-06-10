import urllib.parse
import random

def generate_image(prompt: str):
    """
    Генерирует изображение, формируя URL для API Pollinations.ai.
    Возвращает (URL, None) или (None, ошибка).
    """
    try:
        # Убираем лишние слова типа "нарисуй", чтобы промпт был точнее
        clean_prompt = prompt.lower().replace("нарисуй", "").strip()
        if not clean_prompt:
            clean_prompt = "beautiful picture"

        # Кодируем промпт для URL
        encoded_prompt = urllib.parse.quote(clean_prompt)

        # Добавляем случайный seed, чтобы избегать кэширования одинаковых промптов
        seed = random.randint(1, 1000000)

        # Формируем URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
