import urllib.parse
import random

def generate_image_url(prompt):
    # Base URL for pollinations.ai image generation
    base_url = "https://image.pollinations.ai/prompt/"

    # URL-encode the prompt
    encoded_prompt = urllib.parse.quote(prompt)

    # Append a random seed to prevent caching identical prompts
    seed = random.randint(1, 1000000)

    # Construct the final URL
    url = f"{base_url}{encoded_prompt}?seed={seed}&nologo=true"

    return url
