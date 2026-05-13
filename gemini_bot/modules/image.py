import urllib.parse
import random

def generate_image_url(prompt):
    """
    Generates an image URL using the Pollinations.ai API.
    URL encodes the prompt and appends a random seed to prevent caching.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Construct the URL based on Pollinations.ai format
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
        return url, None
    except Exception as e:
        return None, f"Failed to construct image URL: {e}"
