import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Constructs an image URL using the Pollinations.ai API based on the prompt.
    Returns a tuple of (image_url, error_message).
    """
    try:
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Append a random seed to prevent caching identical prompts
        seed = random.randint(1, 1000000)

        # Construct the pollinations image URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=true"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
