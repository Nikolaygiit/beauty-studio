import urllib.parse
import random

class ImageGeneration:
    def __init__(self):
        self.base_url = "https://pollinations.ai/p/"

    def generate(self, prompt, width=1024, height=1024, seed=None, model="flux"):
        """
        Generates an image URL using Pollinations.ai.
        Args:
            prompt (str): The text description of the image.
            width (int): Image width.
            height (int): Image height.
            seed (int): Random seed.
            model (str): Model to use (flux, turbo, etc).
        Returns:
            str: The URL of the generated image.
        """
        if seed is None:
            seed = random.randint(0, 100000)

        encoded_prompt = urllib.parse.quote(prompt)
        url = f"{self.base_url}{encoded_prompt}?width={width}&height={height}&model={model}&seed={seed}&nologo=true"
        return url
