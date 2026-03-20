import random
import requests
from io import BytesIO
from PIL import Image
import urllib.parse
import streamlit as st

def generate_image(prompt: str):
    """
    Generate an image using Pollinations.ai.
    Appends a random seed to prevent caching identical prompts.
    """
    try:
        seed = random.randint(1, 1000000)
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1024&height=1024"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        image = Image.open(BytesIO(response.content))
        return image, None
    except Exception as e:
        return None, f"Error generating image: {e}"
