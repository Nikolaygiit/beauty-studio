import urllib.parse
import random

def generate_image(prompt):
    """Generates an image URL using the Pollinations.ai API."""
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    # The URL pattern for Pollinations.ai is https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
    return image_url
