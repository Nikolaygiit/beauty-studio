import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Generates an image using Pollinations.ai based on the prompt.
    Appends a random seed to prevent caching of identical prompts.
    """
    seed = random.randint(1, 100000)
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
    return url
