import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Generates an image using Pollinations.ai.
    Returns a tuple of (image_url, error_message).
    """
    if not prompt:
        return None, "Prompt is required to generate an image."

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Using Pollinations.ai API URL construction
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        return image_url, None
    except Exception as e:
        return None, f"Failed to generate image: {e}"
