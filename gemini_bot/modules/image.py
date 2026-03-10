import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt):
    try:
        url = f"https://image.pollinations.ai/prompt/{prompt}"
        response = requests.get(url)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        return f"Произошла ошибка при генерации изображения: {str(e)}"
