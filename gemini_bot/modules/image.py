import urllib.parse
import random
from typing import Tuple, Optional

def generate_image(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates an image via Pollinations.ai API construction.
    Returns (url, error_message).
    """
    try:
        # Properly URL-encode the prompt and append a random seed to prevent caching
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {e}"
