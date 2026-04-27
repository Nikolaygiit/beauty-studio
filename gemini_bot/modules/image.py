import urllib.parse
import random

def generate_image(prompt):
    """
    Формирует URL для генерации картинки через Pollinations.ai.
    Используем прямое формирование URL без requests,
    чтобы избежать 403 Forbidden Cloudflare.
    """
    try:
        # Кодируем промпт для URL
        encoded_prompt = urllib.parse.quote(prompt)
        # Добавляем случайный сид для обхода кэширования одинаковых промптов
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
        return image_url, None
    except Exception as e:
        return None, f"Ошибка формирования URL для изображения: {e}"
