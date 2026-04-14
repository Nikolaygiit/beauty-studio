import urllib.parse
import random

def generate_image_url(prompt):
    """
    Генерирует ссылку на изображение с помощью Pollinations.ai API.
    Использует случайный seed для избежания кэширования.
    Возвращает URL-адрес картинки.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    # Формируем URL в соответствии с API Pollinations.ai
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return image_url
