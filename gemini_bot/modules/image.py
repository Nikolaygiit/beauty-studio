import random
import urllib.parse

def generate_image_url(prompt):
    """
    Generates a Pollinations.ai URL for the given prompt.
    Appends a random seed to prevent caching identical prompts.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"
    return image_url
