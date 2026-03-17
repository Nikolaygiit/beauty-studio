import urllib.parse
import random

def generate_image_url(prompt):
    """
    Генерирует URL для изображения через Pollinations.ai.
    Добавляет случайный seed, чтобы избежать кеширования идентичных промптов.
    """
    seed = random.randint(1, 100000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
