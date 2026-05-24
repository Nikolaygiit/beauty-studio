import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates an image via Pollinations.ai API by constructing a URL.
    Returns (url, error_message)
    """
    try:
        # URL-encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)

        # Append a random seed to prevent caching identical prompts
        seed = random.randint(1, 999999999)

        # Construct the URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
