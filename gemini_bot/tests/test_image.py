from modules.image import generate_image
import urllib.parse

def test_generate_image_empty_prompt():
    url, error = generate_image("")
    assert url is None
    assert "Prompt cannot be empty" in error

def test_generate_image_valid_prompt():
    prompt = "A beautiful sunset over the ocean"
    url, error = generate_image(prompt)

    assert error is None
    assert url.startswith("https://image.pollinations.ai/prompt/")
    encoded_prompt = urllib.parse.quote(prompt)
    assert encoded_prompt in url
    assert "seed=" in url
    assert "nologo=true" in url
