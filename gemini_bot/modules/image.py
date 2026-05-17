import urllib.parse
import random

def generate_image_url(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 100000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
    return url, None
