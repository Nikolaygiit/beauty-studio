import random
import urllib.parse

def generate_image(prompt):
    """
    Generate an image using Pollinations.ai API with a random seed.
    """
    try:
        seed = random.randint(1, 1000000)
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
        return url
    except Exception as e:
        return f"Произошла ошибка при генерации изображения: {str(e)}"
