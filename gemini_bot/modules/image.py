import urllib.parse
import random

def generate_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
    return url
