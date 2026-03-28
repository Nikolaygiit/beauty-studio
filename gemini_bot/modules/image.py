import urllib.parse
import random

def get_image_url(prompt):
    """
    Generate image URL via Pollinations.ai based on the prompt.
    Appends a random seed to prevent caching identical prompts.
    """
    try:
        # URL encode the prompt
        encoded_prompt = urllib.parse.quote(prompt)
        # Generate random seed
        seed = random.randint(1, 1000000)
        # Construct the pollinations URL
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024&nologo=True"
        return url
    except Exception as e:
        return f"Ошибка при генерации изображения: {str(e)}"
