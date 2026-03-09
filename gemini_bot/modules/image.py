import urllib.parse

def generate_image(prompt):
    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
    return url