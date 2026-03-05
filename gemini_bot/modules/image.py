import urllib.parse
import random

class ImageGenerator:
    def __init__(self):
        self.base_url = "https://image.pollinations.ai/prompt/"

    def generate(self, prompt: str) -> str:
        # Generate a random seed to ensure unique images for the same prompt
        seed = random.randint(1, 1000000)

        # URL encode the prompt to safely include it in the URL
        encoded_prompt = urllib.parse.quote(prompt)

        # Construct the final URL with the encoded prompt and seed
        image_url = f"{self.base_url}{encoded_prompt}?seed={seed}&nologo=True"

        return image_url
