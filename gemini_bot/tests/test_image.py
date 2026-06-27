from modules.image import generate_image
import urllib.parse

def test_generate_image_success(mocker):
    # Mock random to have a predictable seed
    mocker.patch('random.randint', return_value=123)

    url, error = generate_image("test prompt")

    assert error is None
    assert "https://image.pollinations.ai/prompt/test%20prompt?seed=123" in url
    assert "width=1024" in url

def test_generate_image_error(mocker):
    # Force an exception by mocking quote to raise ValueError
    mocker.patch('urllib.parse.quote', side_effect=Exception("Test Error"))

    url, error = generate_image("test prompt")

    assert url is None
    assert "Ошибка при создании изображения: Test Error" in error
