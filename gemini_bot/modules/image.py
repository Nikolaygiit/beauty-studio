import requests
import random
import time

def generate_image(prompt, width=1024, height=1024, seed=None, model="flux"):
    """
    Generates an image using Pollinations.ai.

    Args:
        prompt (str): The description of the image.
        width (int): Image width.
        height (int): Image height.
        seed (int): Random seed.
        model (str): Model to use (e.g., 'flux', 'turbo').

    Returns:
        bytes: The image data if successful.
        None: If failed.
    """
    if seed is None:
        seed = random.randint(0, 1000000)

    # Pollinations.ai uses the prompt in the URL path
    # We need to ensure the prompt is safe for URL
    # Using requests.utils.quote is good practice

    # Clean prompt slightly to avoid path issues
    clean_prompt = prompt.replace("/", " ")
    encoded_prompt = requests.utils.quote(clean_prompt)

    base_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    params = {
        "width": width,
        "height": height,
        "seed": seed,
        "model": model,
        "nologo": "true"
    }

    try:
        response = requests.get(base_url, params=params, timeout=60)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception during image generation: {e}")
        return None
