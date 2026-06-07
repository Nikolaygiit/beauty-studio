import urllib.parse
import random

def generate_image(prompt: str):
    """
    Generates an image URL using Pollinations.ai based on the prompt.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
