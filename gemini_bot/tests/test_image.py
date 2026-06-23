from modules.image import generate_image
import urllib.parse

def test_generate_image_success():
    prompt = "beautiful sunset"
    url, err = generate_image(prompt)
    assert err is None
    assert "https://image.pollinations.ai/prompt/" in url
    assert urllib.parse.quote(prompt) in url
    assert "seed=" in url
    assert "nologo=true" in url
