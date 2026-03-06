import requests
from io import BytesIO
from PIL import Image

def generate_image(prompt: str) -> Image.Image:
    """
    Generates an image using Pollinations.ai API.
    """
    # Replace spaces with %20 for URL encoding
    encoded_prompt = prompt.replace(" ", "%20")
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    response = requests.get(url)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    return image
