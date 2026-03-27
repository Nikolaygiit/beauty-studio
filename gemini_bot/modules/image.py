import random
import urllib.parse

def generate_image_url(prompt):
    seed = random.randint(1, 1000000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return url
