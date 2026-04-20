import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using Pollinations.ai API.
    Returns (url, None)
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(0, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return url, None
