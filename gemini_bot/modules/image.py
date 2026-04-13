import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    We encode the prompt and append a random seed to avoid caching.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
