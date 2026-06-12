import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Generates an image URL from Pollinations.ai.
    Returns (url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 9999999)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
