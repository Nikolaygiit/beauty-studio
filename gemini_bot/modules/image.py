import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Constructs a Pollinations.ai URL for the given prompt.
    Returns (image_url, None)
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 100000)
    image_url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}"
    return image_url, None
