import pytest
import urllib.parse
from modules.image import generate_image

def test_generate_image_success(mocker):
    # Mock random to return a fixed seed
    mocker.patch('random.randint', return_value=12345)

    url, error = generate_image("кот в космосе")

    assert error is None
    assert url is not None
    encoded_prompt = urllib.parse.quote("кот в космосе")
    assert f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed=12345" == url

def test_generate_image_failure(mocker):
    # Mock urllib.parse.quote to raise an exception
    mocker.patch('urllib.parse.quote', side_effect=Exception("Encoding error"))

    url, error = generate_image("test prompt")

    assert url is None
    assert "Ошибка при генерации изображения: Encoding error" in error
