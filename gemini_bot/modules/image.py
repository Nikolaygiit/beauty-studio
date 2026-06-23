import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Generates an image using Pollinations.ai by creating a URL.
    Returns (url, error_message)
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
        return url, None
    except Exception as e:
        return None, f"Failed to generate image URL: {e}"
