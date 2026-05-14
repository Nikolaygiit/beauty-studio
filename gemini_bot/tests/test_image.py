import pytest
from modules.image import generate_image_url
import urllib.parse

def test_generate_image_url():
    prompt = "beautiful sunset"
    url, error = generate_image_url(prompt)

    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert urllib.parse.quote(prompt) in url
    assert "seed=" in url
    assert "&nologo=True" in url
