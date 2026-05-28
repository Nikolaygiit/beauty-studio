import pytest
from unittest.mock import patch
from modules.image import generate_image

def test_generate_image():
    prompt = "собака в космосе"
    image_url, error = generate_image(prompt)
    assert image_url is not None
    assert error is None
    assert "image.pollinations.ai" in image_url
    assert "prompt/%D1%81%D0%BE%D0%B1%D0%B0%D0%BA%D0%B0%20%D0%B2%20%D0%BA%D0%BE%D1%81%D0%BC%D0%BE%D1%81%D0%B5" in image_url
    assert "seed=" in image_url

def test_generate_image_error():
    with patch('modules.image.urllib.parse.quote') as mock_quote:
        mock_quote.side_effect = Exception("Test error")
        image_url, error = generate_image("test prompt")
        assert image_url is None
        assert "Test error" in error
