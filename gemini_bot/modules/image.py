import urllib.parse
import requests

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        response = requests.get(url)
        response.raise_for_status()
        return response.content
    except Exception as e:
        return f"An error occurred: {e}"
