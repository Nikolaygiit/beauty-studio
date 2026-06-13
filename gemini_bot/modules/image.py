import urllib.parse
import random

def generate_image_url(prompt: str) -> tuple[str, str | None]:
    """
    Generates an image URL using the Pollinations.ai API.
    Properly URL-encodes the prompt and appends a random seed to prevent caching.
    Returns: (image_url, error_message)
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 100000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка создания URL изображения: {str(e)}"
