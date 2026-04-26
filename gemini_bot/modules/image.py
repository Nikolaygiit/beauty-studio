import urllib.parse
import random

def generate_image(prompt):
    """Generates an image URL using Pollinations.ai based on the prompt."""
    try:
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Add a random seed to prevent caching
        seed = random.randint(1, 100000)

        # Construct the URL
        image_url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        # Return the URL, no error
        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
