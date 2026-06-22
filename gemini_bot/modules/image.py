import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str | None]:
    """
    Generates an image URL using the Pollinations.ai API based on the text prompt.
    Returns a tuple of (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
