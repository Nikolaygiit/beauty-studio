from modules.image import generate_image
import urllib.parse

def test_generate_image(mocker):
    # Mock random.randint to always return a predictable seed (e.g., 42)
    mocker.patch('modules.image.random.randint', return_value=42)

    prompt = "космический кот"
    encoded_prompt = urllib.parse.quote(prompt)

    url, error = generate_image(prompt)

    assert error is None
    assert f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed=42" in url
