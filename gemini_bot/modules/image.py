import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates a Pollinations.ai image URL for the given prompt.
    The prompt is URL-encoded and a random seed is appended to prevent caching.
    """
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)

    # Generate a random seed
    seed = random.randint(1, 1000000)

    # Construct the image URL
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"

    return image_url
