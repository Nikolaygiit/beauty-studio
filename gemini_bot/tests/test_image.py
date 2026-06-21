from modules.image import generate_image
import urllib.parse

def test_generate_image_success():
    prompt = "красивый закат"
    url, error = generate_image(prompt)
    assert error is None
    assert url is not None
    assert "image.pollinations.ai" in url
    assert urllib.parse.quote(prompt) in url
    assert "nologo=true" in url
    assert "seed=" in url
