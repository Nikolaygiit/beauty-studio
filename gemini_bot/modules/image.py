import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates an image URL using Pollinations.ai.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(0, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
