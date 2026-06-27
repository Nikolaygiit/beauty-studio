import urllib.parse
import random

def generate_image(prompt: str):
    """
    Generates an image URL using Pollinations.ai.
    Returns (image_url, error_message).
    """
    try:
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        # Append a random seed to prevent caching identical prompts
        seed = random.randint(1, 1000000)

        # Construct the URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при создании изображения: {str(e)}"
