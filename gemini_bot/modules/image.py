import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Generate an image using Pollinations.ai API.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Using Pollinations.ai which handles URL encoded prompts directly
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=True"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
