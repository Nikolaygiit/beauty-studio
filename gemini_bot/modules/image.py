import random
import urllib.parse

def generate_image_url(prompt: str) -> str:
    """Generates an image URL using Pollinations.ai API."""
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    width = 1024
    height = 1024
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width={width}&height={height}&nologo=true"
    return url
