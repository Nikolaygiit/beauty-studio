import pytest
import sys
import os

# Ensure the correct path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import detect_media_intent

def test_detect_media_intent_image():
    # Test keywords for image
    assert detect_media_intent("нарисуй кота") == 'image'
    assert detect_media_intent("сделай ФОТО природы") == 'image'
    assert detect_media_intent("покажи красивое изображение") == 'image'

def test_detect_media_intent_music():
    # Test keywords for music
    assert detect_media_intent("включи музыку") == 'music'
    assert detect_media_intent("спой песню") == 'music'
    assert detect_media_intent("классная песня") == 'music'
    assert detect_media_intent("крутой трек") == 'music'
    assert detect_media_intent("поставь песню!") == 'music'
    # testing morphology
    assert detect_media_intent("послушать песни") == 'music'

def test_detect_media_intent_video():
    # Test keywords for video
    assert detect_media_intent("сними видео") == 'video'
    assert detect_media_intent("покажи ролик") == 'video'

def test_detect_media_intent_text():
    # Test no keywords
    assert detect_media_intent("расскажи сказку") is None
    assert detect_media_intent("привет как дела?") is None
    assert detect_media_intent("какая погода?") is None
