import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Генерирует URL изображения на основе запроса пользователя с использованием Pollinations.ai.
    Добавляет случайный seed для предотвращения кэширования одинаковых запросов.
    """
    seed = random.randint(1, 1000000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
