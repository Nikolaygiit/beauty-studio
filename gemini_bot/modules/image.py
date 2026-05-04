import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using Pollinations.ai based on the prompt.
    Properly URL-encodes the prompt (which might contain Russian) and adds a random seed.
    """
    try:
        # Generate a random seed to avoid caching
        seed = random.randint(1, 1000000)

        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Construct the URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
