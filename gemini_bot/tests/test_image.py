import urllib.parse
from modules.image import generate_image_url

def test_generate_image_url():
    prompt = "собака в космосе"
    encoded_prompt = urllib.parse.quote(prompt)
    url, err = generate_image_url(prompt)

    assert err is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert encoded_prompt in url
    assert "?seed=" in url
    assert "&nologo=true" in url
