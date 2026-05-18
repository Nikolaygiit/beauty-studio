import urllib.parse
import random

def generate_image(prompt: str):
    """
    Constructs a Pollinations.ai image URL.
    Returns (url, None).
    """
    try:
        # Encode the prompt to be safely used in a URL
        encoded_prompt = urllib.parse.quote(prompt)

        # Add a random seed to prevent aggressive caching from giving the same image
        seed = random.randint(1, 1000000)

        # Construct the pollinations URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=True"

        return url, None
    except Exception as e:
        return None, str(e)
