import urllib.parse

def generate_image(prompt):
    """
    Generates an image URL using Pollinations.ai.

    Args:
        prompt (str): The prompt for the image.

    Returns:
        str: The URL of the generated image.
    """
    encoded_prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}"
