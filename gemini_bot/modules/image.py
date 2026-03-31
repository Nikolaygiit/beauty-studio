import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates a URL for Pollinations.ai image generation.
    It properly URL-encodes the prompt and appends a random seed to prevent caching identical prompts.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 999999999)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
    return url
