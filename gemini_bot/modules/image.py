import urllib.parse
import random

def generate_image_url(prompt: str) -> tuple[str, str | None]:
    """
    Generates a Pollinations.ai image URL based on the prompt.
    Returns (url, None).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
