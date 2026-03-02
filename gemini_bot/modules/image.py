import urllib.parse
import uuid

def generate_image_url(prompt: str) -> str:
    """
    Generates an image URL using the Pollinations.ai API based on the prompt.
    Appends a random seed to avoid caching identical prompts.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    random_seed = uuid.uuid4().hex[:8] # Add random seed for uniqueness
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=1&seed={random_seed}"
    return url
