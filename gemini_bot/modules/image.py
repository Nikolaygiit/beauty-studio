import urllib.parse
import random
from typing import Tuple

def generate_image(prompt: str) -> Tuple[str, str]:
    """
    Generates an image using Pollinations.ai API by constructing a URL.
    Returns (media_url, error_message).
    """
    try:
        # Encode the prompt properly
        encoded_prompt = urllib.parse.quote(prompt)

        # Append a random seed to prevent caching identical prompts
        seed = random.randint(1, 1000000)

        # Construct the URL for Pollinations.ai
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return image_url, ""
    except Exception as e:
        return "", f"Ошибка генерации изображения: {str(e)}"
