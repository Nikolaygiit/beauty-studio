import urllib.parse
import uuid

def generate_image_url(prompt):
    """
    Generates an image URL using the Pollinations.ai API based on the prompt.
    Adds a random UUID to avoid caching issues on the frontend.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    random_seed = uuid.uuid4().hex
    # Adding an explicit width/height and seed to bypass potential caches and get standard output
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={random_seed}"
    return url
