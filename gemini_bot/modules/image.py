import urllib.parse
import random

def generate_image_url(prompt: str) -> str:
    """
    Generates a URL for Pollinations.ai image generation based on the prompt.
    Appends a random seed to prevent caching identical prompts.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    # The URL needs to be passed directly to the frontend (e.g. st.image)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=true"
    return url

def generate_image(prompt: str) -> tuple[str, str]:
    """
    Wrapper function to maintain signature consistency with other media generation modules.
    Returns (url, error_message).
    """
    try:
        url = generate_image_url(prompt)
        return url, None
    except Exception as e:
        return None, f"Ошибка генерации ссылки на изображение: {e}"
