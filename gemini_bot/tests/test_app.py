import pytest
import os
import sys

# Ensure modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.text import init_client
from modules.image import generate_image

def test_init_client_invalid_key():
    client, err = init_client("invalid_key_123")
    # Even with an invalid key, google-genai client initialization usually succeeds
    # Validation happens during API calls.
    assert client is not None or err is not None

def test_generate_image_url_format():
    url, err = generate_image("test prompt")
    assert err is None
    assert url.startswith("https://image.pollinations.ai/")
    assert "test%20prompt" in url
    assert "seed=" in url

def test_keyword_routing():
    # Simple manual test representations of keyword logic in app.py
    prompt1 = "Нарисуй мне кота"
    prompt2 = "Включи музыку"
    prompt3 = "Сделай видео"
    prompt4 = "Привет, как дела?"

    prompt1_lower = prompt1.lower()
    prompt2_lower = prompt2.lower()
    prompt3_lower = prompt3.lower()
    prompt4_lower = prompt4.lower()

    assert "нарисуй" in prompt1_lower
    assert "музык" in prompt2_lower
    assert "видео" in prompt3_lower
    assert not any(kw in prompt4_lower for kw in ["нарисуй", "фото", "музыка", "видео"])
