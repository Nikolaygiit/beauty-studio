import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using Pollinations.ai API.
    Returns (image_url, None) on success, or (None, error_message) on failure.
    """
    try:
        # Encode the prompt for URL
        encoded_prompt = urllib.parse.quote(prompt)

        # Append a random seed to avoid caching
        seed = random.randint(1, 1000000)

        # Construct the URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
