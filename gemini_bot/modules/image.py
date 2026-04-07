import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Generates an image URL from Pollinations.ai based on the prompt.
    Properly URL-encodes the prompt and appends a random seed.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    # Pollinations.ai URL format: https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return url
