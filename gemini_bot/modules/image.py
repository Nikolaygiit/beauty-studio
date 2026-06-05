import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Generates an image using Pollinations.ai API by constructing a URL.
    Returns the URL directly so the frontend can display it.
    """
    # Append a random seed to prevent caching identical prompts
    seed = random.randint(1, 1000000)

    # URL encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)

    # Construct the Pollinations URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

    return url
