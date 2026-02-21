import requests
import io
from PIL import Image

class ImageGenerator:
    def __init__(self):
        self.base_url = "https://pollinations.ai/p/"

    def generate(self, prompt, width=1024, height=1024, seed=None):
        encoded_prompt = requests.utils.quote(prompt)
        url = f"{self.base_url}{encoded_prompt}"

        seed_val = seed if seed else 42
        final_url = f"{url}?width={width}&height={height}&seed={seed_val}&nologo=true"

        try:
            response = requests.get(final_url)
            response.raise_for_status()
            image_bytes = io.BytesIO(response.content)
            image = Image.open(image_bytes)
            return image
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
