import urllib.parse
import random

def generate_image(prompt: str):
    """
    Constructs a Pollinations.ai URL for image generation.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        return url, None
    except Exception as e:
        return None, f"Error constructing image URL: {str(e)}"
