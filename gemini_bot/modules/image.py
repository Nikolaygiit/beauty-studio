import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL from pollinations.ai.
    The prompt is URL-encoded, and a random seed is appended to avoid caching.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return image_url
