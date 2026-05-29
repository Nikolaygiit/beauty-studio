import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str, str | None]:
    """
    Generates an image URL using the Pollinations.ai API based on the prompt.
    Returns: (url, None)
    """
    try:
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Add a random seed to prevent caching
        seed = random.randint(1, 1000000)

        # Construct the URL
        url = f"https://pollinations.ai/p/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"

        return url, None
    except Exception as e:
        return "", f"Ошибка при генерации изображения: {str(e)}"
