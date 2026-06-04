import pytest
import urllib.parse
from gemini_bot.modules.image import generate_image

def test_image_generation_url():
    prompt = "собака играет в парке"
    url, error = generate_image(prompt)

    assert error is None
    assert url is not None
    assert url.startswith("https://image.pollinations.ai/prompt/")

    encoded_prompt = urllib.parse.quote(prompt)
    assert encoded_prompt in url
    assert "seed=" in url
    assert "nologo=true" in url
