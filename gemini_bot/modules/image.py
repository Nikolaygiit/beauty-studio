import urllib.parse
import random

def generate_image_url(prompt: str) -> str:
    """
    Generates an image URL using the pollinations.ai API based on the prompt.
    Appends a random seed to prevent caching if the same prompt is requested twice.
    """
    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)

    # Construct the URL
    # Width and height can be customized if needed, defaulting to square 1024x1024
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=True"

    return image_url
