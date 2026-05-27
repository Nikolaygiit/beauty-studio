import urllib.parse
import pytest
from unittest.mock import patch
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

def test_image_url_generation():
    prompt = "красивый кот"
    url = generate_image_url(prompt)
    assert "https://image.pollinations.ai/prompt/" in url
    assert "%20" in url or "кот" in urllib.parse.unquote(url)
    assert "seed=" in url

def test_russian_keyword_routing():
    image_keywords = ['нарисуй', 'фото', 'изображение']
    music_keywords = ['музык', 'песн', 'песен', 'трек']
    video_keywords = ['видео', 'ролик']

    # Test morphology and exact matches
    test_cases = [
        ("нарисуй мне дом", image_keywords, True),
        ("покажи фото кота", image_keywords, True),
        ("создай изображение леса", image_keywords, True),
        ("включи музыку", music_keywords, True),
        ("спой песню", music_keywords, True),
        ("сочини много песен", music_keywords, True),
        ("запиши крутой трек", music_keywords, True),
        ("сними видео", video_keywords, True),
        ("сделай ролик", video_keywords, True),
        ("просто текст", image_keywords + music_keywords + video_keywords, False)
    ]

    for prompt, keywords, should_match in test_cases:
        prompt_lower = prompt.lower()
        matched = any(kw in prompt_lower for kw in keywords)
        assert matched == should_match, f"Failed routing test for prompt: '{prompt}'"

@patch('modules.music.get_music_client')
def test_mock_music_generation(mock_get_client):
    class MockClient:
        def predict(self, **kwargs):
            return "/path/to/mock_audio.wav"

    mock_get_client.return_value = MockClient()
    result, error = generate_music("тестовая песня")

    assert result == "/path/to/mock_audio.wav"
    assert error is None

@patch('modules.video.get_video_client')
def test_mock_video_generation(mock_get_client):
    class MockClient:
        def predict(self, *args, **kwargs):
            return "/path/to/mock_video.mp4"

    mock_get_client.return_value = MockClient()
    result, error = generate_video("тестовое видео")

    assert result == "/path/to/mock_video.mp4"
    assert error is None
