import pytest
from modules.image import generate_image_url
import urllib.parse

def test_generate_image_url(mocker):
    # Mock random.randint to always return 12345
    mocker.patch('random.randint', return_value=12345)

    prompt = "нарисуй кота"
    url, err = generate_image_url(prompt)

    assert err is None
    expected_encoded = urllib.parse.quote(prompt)
    assert url == f"https://image.pollinations.ai/prompt/{expected_encoded}?seed=12345"

def test_generate_image_url_exception(mocker):
    # Mock urllib.parse.quote to raise an exception
    mocker.patch('urllib.parse.quote', side_effect=Exception("Encode error"))

    url, err = generate_image_url("test")

    assert url is None
    assert err == "Ошибка создания URL изображения: Encode error"
