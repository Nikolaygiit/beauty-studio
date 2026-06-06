import urllib.parse
import random

def generate_image(prompt: str) -> tuple[str | None, str | None]:
    """
    Returns a Pollinations.ai URL for the generated image and an optional error message.
    The URL is returned instead of downloading it directly to bypass Cloudflare 403 errors.
    """
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&nologo=True"
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации изображения: {str(e)}"
