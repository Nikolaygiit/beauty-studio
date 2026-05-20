import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, None]:
    """
    Generates an image URL using Pollinations.ai API.
    URL-encodes the prompt and adds a random seed to prevent caching.
    Returns a tuple of (url, error_message).
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"

    # We return (URL, None) to match the (result, error) pattern of other media generators
    return url, None
