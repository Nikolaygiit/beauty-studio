import pytest
from modules.image import generate_image

def test_generate_image_success(mocker):
    mocker.patch('modules.image.random.randint', return_value=123)
    url, error = generate_image("test prompt")

    assert "https://image.pollinations.ai/prompt/test%20prompt?seed=123&nologo=True" == url
    assert error is None
