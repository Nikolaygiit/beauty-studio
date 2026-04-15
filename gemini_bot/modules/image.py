import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Generates an image URL using Pollinations.ai based on the prompt.
    The URL encodes the prompt and appends a random seed to avoid caching.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 10000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return url
