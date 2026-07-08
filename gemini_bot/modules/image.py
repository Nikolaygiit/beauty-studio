import urllib.parse
import random

def generate_image(prompt: str):
    """
    Generates an image URL using Pollinations.ai.
    URL encodes the prompt and appends a random seed to avoid caching.
    Returns (url, error_message).
    """
    try:
        if not prompt:
            return None, "Prompt cannot be empty"

        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        return url, None
    except Exception as e:
        return None, str(e)
