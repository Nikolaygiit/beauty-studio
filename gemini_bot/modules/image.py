import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using Pollinations.ai.
    Properly URL-encodes the prompt and appends a random seed.
    Returns (url, error_message)
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}&width=1024&height=1024"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
