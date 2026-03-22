import urllib.parse
import random

def generate_image_url(prompt: str) -> str:
    """
    Generates an image URL using the Pollinations.ai API.
    A random seed is appended to prevent browser caching of identical prompts.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(0, 100000)
    # The Pollinations.ai URL format is https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return image_url
