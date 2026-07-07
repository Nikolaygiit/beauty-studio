from modules.image import generate_image
import urllib.parse

def test_generate_image(mocker):
    # Mock random.randint to have a predictable seed
    mocker.patch("modules.image.random.randint", return_value=12345)

    prompt = "Красивый кот"
    expected_encoded = urllib.parse.quote(prompt)
    url, error = generate_image(prompt)

    assert error is None
    assert expected_encoded in url
    assert "seed=12345" in url
    assert url == f"https://image.pollinations.ai/prompt/{expected_encoded}?seed=12345"
