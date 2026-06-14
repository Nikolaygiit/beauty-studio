import urllib.parse
from modules.image import generate_image_url

def test_generate_image_url(mocker):
    # Mock random.randint to always return a specific seed
    mocker.patch('modules.image.random.randint', return_value=12345)

    prompt = "собака в космосе"
    expected_encoded = urllib.parse.quote(prompt)
    expected_url = f"https://image.pollinations.ai/prompt/{expected_encoded}?seed=12345"

    result_url = generate_image_url(prompt)

    assert result_url == expected_url
