import pytest
import urllib.parse
from modules.image import generate_image

def test_generate_image(mocker):
    # Mock random.randint to have predictable seed
    mocker.patch("modules.image.random.randint", return_value=12345)

    prompt = "красивый кот"
    url, err = generate_image(prompt)

    expected_encoded = urllib.parse.quote(prompt)
    assert url == f"https://image.pollinations.ai/prompt/{expected_encoded}?seed=12345"
    assert err is None
