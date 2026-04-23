import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    The prompt is URL-encoded, and a random seed is appended to prevent caching.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Using Pollinations.ai as specified
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {e}"