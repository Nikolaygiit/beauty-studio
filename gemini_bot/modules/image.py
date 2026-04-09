import urllib.parse
import random

def generate_image(prompt):
    """Generates an image by constructing a Pollinations.ai URL."""
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return image_url
