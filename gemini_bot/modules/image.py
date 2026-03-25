import urllib.parse
import random
import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt):
    """Generates an image using Pollinations.ai API."""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(0, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        return f"**Ошибка при генерации изображения:** {e}"
