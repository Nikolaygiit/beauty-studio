import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    Appends a random seed to prevent caching identical prompts.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Assuming typical Pollinations.ai URL structure
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return image_url
    except Exception as e:
        return f"Ошибка генерации изображения: {e}"
