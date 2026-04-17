import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL from Pollinations.ai based on the prompt.
    Returns the URL directly for frontend rendering.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url
