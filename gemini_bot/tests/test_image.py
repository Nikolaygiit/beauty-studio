from modules.image import generate_image
import urllib.parse

def test_generate_image(mocker):
    # Mock random.randint to always return a specific seed
    mocker.patch("random.randint", return_value=12345)

    prompt = "красивый кот"
    url, error = generate_image(prompt)

    encoded_prompt = urllib.parse.quote(prompt)
    expected_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed=12345&nologo=True"

    assert url == expected_url
    assert error is None

def test_generate_image_error(mocker):
    mocker.patch("urllib.parse.quote", side_effect=Exception("Encoding error"))

    url, error = generate_image("test")
    assert url is None
    assert "Ошибка при генерации изображения: Encoding error" in error
