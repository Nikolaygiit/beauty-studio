import urllib.parse
import random

def generate_image(prompt):
    try:
        # Proper URL encoding to handle spaces and special characters
        encoded_prompt = urllib.parse.quote(prompt)
        # Adding a random seed prevents Pollinations.ai from caching the exact same prompt
        seed = random.randint(1, 1000000)

        # Build the final URL (we return the URL directly for the frontend to render, per memory instructions)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}"

        return image_url, None
    except Exception as e:
        return None, f"Ошибка при генерации изображения: {e}"
