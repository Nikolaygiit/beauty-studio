import urllib.parse
import random

def generate_image(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    URL-encodes the prompt and appends a random seed to prevent caching.
    Returns a tuple (image_url, error_message).
    """
    if not prompt:
        return None, "Prompt is missing."

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"
        return url, None
    except Exception as e:
        return None, f"Failed to generate image URL: {str(e)}"
