import urllib.parse
import random
from typing import Tuple, Optional

def generate_image(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates an image URL using the Pollinations.ai service.

    Returns a tuple of (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        # Adding a random seed prevents caching identical prompts
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
