import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates an image via the Pollinations.ai API.
    Returns a tuple of (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
