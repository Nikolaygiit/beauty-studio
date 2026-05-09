import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Constructs a Pollinations.ai URL for image generation.
    Returns (url, error_message).
    """
    try:
        # URL-encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Generate a random seed to prevent caching
        seed = random.randint(1, 1000000)

        # Construct the Pollinations URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {e}"
