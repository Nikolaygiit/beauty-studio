import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates an image URL using the Pollinations.ai API.
    Returns a tuple of (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
