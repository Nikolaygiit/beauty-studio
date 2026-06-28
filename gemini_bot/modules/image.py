import urllib.parse
import random

def generate_image(prompt: str):
    """
    Generates an image URL using the Pollinations.ai API.
    URL encodes the prompt and appends a random seed to prevent caching.
    Returns (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 100000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
