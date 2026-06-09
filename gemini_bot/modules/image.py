import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str | None]:
    """
    Generates an image URL using the Pollinations.ai API.
    URL-encodes the prompt and adds a random seed to prevent caching.
    Returns:
        tuple: (url, error_message)
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
        return url, None
    except Exception as e:
        return "", f"Ошибка при генерации изображения: {str(e)}"
