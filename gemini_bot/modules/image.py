import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image using the Pollinations.ai API based on the text prompt.
    Returns the URL to the generated image.
    """
    seed = random.randint(1, 1000000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
    return url
