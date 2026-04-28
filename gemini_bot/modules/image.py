import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates a Pollinations.ai image URL for the given prompt.
    The URL includes URL-encoding and a random seed to prevent caching.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
    return url
