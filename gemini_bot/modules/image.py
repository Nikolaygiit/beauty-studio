import urllib.parse
import random
from typing import Tuple, Optional

def generate_image(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates an image URL using the Pollinations.ai API.
    Returns:
        (image_url, error_message)
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Using Pollinations.ai with URL-encoded prompt and a random seed to prevent caching
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
