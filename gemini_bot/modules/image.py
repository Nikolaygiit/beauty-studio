import urllib.parse
import random

def generate_image(prompt: str):
    """
    Generates an image URL using Pollinations.ai API.
    Returns (url, error_message).
    """
    try:
        # Encode the prompt for the URL
        encoded_prompt = urllib.parse.quote(prompt)
        # Append a random seed to prevent caching identical prompts
        seed = random.randint(1, 1000000)

        # Construct the URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        # Return the URL directly for the frontend to render, as per memory instructions
        return url, None
    except Exception as e:
        return None, f"Error generating image URL: {e}"
