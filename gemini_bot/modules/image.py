import urllib.parse
import random

def generate_image_url(prompt):
    """Generates an image URL from Pollinations.ai based on the prompt."""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
        return image_url, None
    except Exception as e:
        return None, f"Error generating image URL: {e}"