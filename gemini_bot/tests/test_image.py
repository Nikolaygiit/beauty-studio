import pytest
from modules.image import generate_image
import urllib.parse

def test_generate_image_success(mocker):
    mocker.patch('random.randint', return_value=123)
    prompt = "Test prompt with spaces"
    url, error = generate_image(prompt)

    assert error is None
    assert url == f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?seed=123"

def test_generate_image_error(mocker):
    mocker.patch('urllib.parse.quote', side_effect=Exception("Encode error"))
    url, error = generate_image("test")

    assert url is None
    assert "Encode error" in error
