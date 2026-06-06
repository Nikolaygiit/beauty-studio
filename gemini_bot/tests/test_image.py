from modules.image import generate_image
import urllib.parse

def test_generate_image_url_format():
    prompt = "Тестовый запрос"
    url, error = generate_image(prompt)

    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert urllib.parse.quote(prompt) in url
    assert "nologo=True" in url
    assert "seed=" in url
