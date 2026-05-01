import urllib.parse
import random

def generate_image(prompt: str) -> str:
    """
    Generate an image URL using Pollinations.ai API.

    Args:
        prompt: The text prompt for image generation.

    Returns:
        The URL string for the generated image.
    """
    # URL-encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)

    # Generate a random seed to prevent caching identical prompts
    seed = random.randint(1, 1000000)

    # Construct the URL
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

    return url
