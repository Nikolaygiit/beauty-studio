import urllib.parse
import random

def generate_image_url(prompt):
    """
    Генерация URL изображения с использованием Pollinations.ai.
    """
    seed = random.randint(1, 1000000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
