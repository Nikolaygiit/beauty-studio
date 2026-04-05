import urllib.parse
import random

def generate_image_url(prompt):
    """Generates an image URL using Pollinations.ai based on the prompt."""
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 100000)
    # Append seed to prevent caching
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return url
