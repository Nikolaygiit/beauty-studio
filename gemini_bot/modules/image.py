import urllib.parse
import time
import requests

def generate_image(prompt: str):
    """
    Generates image using pollinations.ai
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = int(time.time() * 1000) % 1000000
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        # Check if the URL is accessible and returns an image
        response = requests.get(url)
        if response.status_code == 200:
            return url
        else:
            return f"Error: Received status code {response.status_code} from image generator."

    except Exception as e:
        return f"Error generating image: {str(e)}"
