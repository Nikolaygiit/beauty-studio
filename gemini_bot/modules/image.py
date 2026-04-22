import urllib.parse
import random

def generate_image_url(prompt: str) -> str:
    """
    Generates an image URL using the Pollinations.ai API based on the prompt.
    URL-encodes the prompt and appends a random seed to prevent caching.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

    return image_url