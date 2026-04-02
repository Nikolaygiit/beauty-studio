import urllib.parse
import random

def get_image_url(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 10000)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&nologo=true"
