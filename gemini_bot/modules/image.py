import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Генерирует изображение через Pollinations.ai.
    Возвращает: (url_изображения, сообщение_об_ошибке)
    """
    try:
        # Кодируем текст запроса для URL
        encoded_prompt = urllib.parse.quote(prompt)
        # Добавляем случайный сид (seed) чтобы избежать кэширования одинаковых запросов
        seed = random.randint(1, 1000000)

        # Формируем URL для Pollinations.ai
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
