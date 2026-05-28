import urllib.parse
import random

def generate_image(prompt: str):
    """Generates an image URL using Pollinations.ai."""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 100000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return image_url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {e}"
