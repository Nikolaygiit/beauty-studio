import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    URL-encodes the prompt and adds a random seed to prevent caching.
    Returns the URL directly, offloading fetching to the browser.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
    return url
