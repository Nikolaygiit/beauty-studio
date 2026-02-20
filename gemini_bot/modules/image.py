import requests
from PIL import Image
from io import BytesIO
import urllib.parse

def generate_image(prompt):
    """
    Generates an image from Pollinations.ai based on the prompt.
    """
    if not prompt:
        return None

    # Encode the prompt for the URL
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
