import urllib.parse
import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        return f"Ошибка генерации изображения: {str(e)}"
