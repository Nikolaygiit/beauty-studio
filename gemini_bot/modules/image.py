import urllib.parse
import random
from typing import Tuple, Optional

def generate_image(prompt: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Generates an image URL using the Pollinations.ai API based on the prompt.
    Returns a tuple of (image_url, error_message).
    """
    try:
        # Encode the prompt for the URL
        encoded_prompt = urllib.parse.quote(prompt)
        # Generate a random seed to prevent caching identical prompts
        seed = random.randint(1, 1000000)

        # Construct the URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
