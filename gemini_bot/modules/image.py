import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Генерирует изображение через Pollinations.ai, формируя URL.
    Возвращает (image_url, error_message).
    Если ошибка отсутствует, error_message будет пустой строкой.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}"
        return image_url, ""
    except Exception as e:
        return None, f"Ошибка формирования ссылки на изображение: {str(e)}"
