import urllib.parse
import random

def generate_image(prompt):
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&n={seed}"
        return url, None
    except Exception as e:
        return None, str(e)
