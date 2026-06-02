import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Constructs an image URL for the prompt using Pollinations.ai API.
    Returns (url, None) on success, or (None, error_message) on failure.
    """
    try:
        # URL-encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Append a random seed to avoid caching
        seed = random.randint(1, 1000000)

        # Construct the URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {str(e)}"
