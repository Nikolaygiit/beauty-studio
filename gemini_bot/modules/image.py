import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str | None]:
    """
    Generates an image URL using the Pollinations.ai API.
    Returns a tuple of (image_url, error_message).
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return image_url, None
    except Exception as e:
        return "", f"Error generating image: {str(e)}"
