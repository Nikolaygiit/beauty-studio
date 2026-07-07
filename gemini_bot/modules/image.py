import urllib.parse
import random
from typing import Tuple, Optional

def generate_image(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates an image URL based on the given prompt using Pollinations.ai.
    URL-encodes the prompt and appends a random seed.
    Returns (url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(0, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
