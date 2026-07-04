import pytest
import urllib.parse
from modules.image import generate_image

def test_generate_image(mocker):
    # Mock random.randint to return a predictable seed
    mocker.patch("modules.image.random.randint", return_value=12345)

    prompt = "beautiful landscape"
    url, error = generate_image(prompt)

    assert error is None
    expected_url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed=12345"
    assert url == expected_url

def test_generate_image_exception(mocker):
    # Mock urllib.parse.quote to raise an exception
    mocker.patch("modules.image.urllib.parse.quote", side_effect=Exception("Test error"))

    url, error = generate_image("test")

    assert url is None
    assert "Test error" in error
