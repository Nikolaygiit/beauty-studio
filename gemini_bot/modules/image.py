import random
import urllib.parse
import logging

def generate_image(prompt: str) -> str:
    """
    Generates an image URL using the Pollinations.ai API.
    A random seed is appended to prevent caching identical prompts.
    """
    try:
        # Encode the prompt for the URL
        encoded_prompt = urllib.parse.quote(prompt)

        # Generate a random seed
        seed = random.randint(1, 1000000)

        # Construct the Pollinations URL
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?nologo=true&seed={seed}"

        return image_url
    except Exception as e:
        error_msg = f"Ошибка генерации изображения: {str(e)}"
        logging.error(error_msg)
        return error_msg
