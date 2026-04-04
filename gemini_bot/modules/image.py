import urllib.parse
import random

def generate_image_url(prompt: str) -> str:
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 100000)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
