import urllib.parse
from PIL import Image
import requests
from io import BytesIO

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        return f"Ошибка генерации изображения: {e}"
