import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    if not prompt:
        return None, "Prompt is required for image generation"

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        # Using Pollinations.ai API
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}"
        return image_url, None
    except Exception as e:
        return None, f"Error generating image: {str(e)}"
