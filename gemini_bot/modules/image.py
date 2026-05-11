import urllib.parse
import random

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 999999999)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
