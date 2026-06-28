from modules.image import generate_image
import urllib.parse

def test_generate_image():
    prompt = "собака в космосе"
    image_url, error = generate_image(prompt)

    assert error is None
    assert "image.pollinations.ai" in image_url
    assert urllib.parse.quote(prompt) in image_url
    assert "seed=" in image_url
