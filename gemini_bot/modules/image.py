import urllib.parse
import random

def generate_image(prompt):
    """
    Generate an image URL from Pollinations.ai using the given prompt.
    Returns the constructed URL.
    """
    seed = random.randint(1, 100000000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
    return url, None
