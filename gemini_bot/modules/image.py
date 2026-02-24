import requests
from io import BytesIO
from PIL import Image
import urllib.parse

def generate_image(prompt, width=1024, height=1024, model="flux"):
    """
    Generates an image using Pollinations.ai API.
    Args:
        prompt (str): The description of the image.
        width (int): Image width.
        height (int): Image height.
        model (str): Model to use (default: flux).
    Returns:
        PIL.Image: The generated image object or None if failed.
    """
    prompt_encoded = urllib.parse.quote(prompt)
    # nologo=true removes the watermark if possible, or seed ensures variety
    url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width={width}&height={height}&model={model}&nologo=true"

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            image_bytes = BytesIO(response.content)
            image = Image.open(image_bytes)
            return image
        else:
            print(f"Error: Status Code {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception generating image: {e}")
        return None
