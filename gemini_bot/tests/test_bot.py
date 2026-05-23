import pytest
from unittest.mock import MagicMock, patch

# Add parent directory to path to allow imports when running tests directly
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.text import init_gemini_client, init_chat_session, SYSTEM_INSTRUCTION
from modules.image import generate_image

def test_system_instruction_russian():
    assert "Russian" in SYSTEM_INSTRUCTION, "System instruction must enforce Russian language."

@patch('google.genai.Client')
def test_init_gemini_client(MockClient):
    # Setup mock
    mock_instance = MockClient.return_value

    # Call function
    client = init_gemini_client("test_api_key")

    # Assert
    assert client == mock_instance
    MockClient.assert_called_once_with(api_key="test_api_key")

def test_init_chat_session():
    # Setup mock client
    mock_client = MagicMock()
    mock_chat = MagicMock()
    mock_client.chats.create.return_value = mock_chat

    # Call function
    chat_session = init_chat_session(mock_client)

    # Assert
    assert chat_session == mock_chat
    mock_client.chats.create.assert_called_once_with(
        model="gemini-2.0-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )

def test_generate_image_url_structure():
    prompt = "Test prompt for image"
    url, err = generate_image(prompt)

    # Assert
    assert err is None
    assert url is not None
    assert "https://image.pollinations.ai/prompt/" in url
    assert "Test%20prompt%20for%20image" in url
    assert "?seed=" in url
    assert "&nologo=True" in url

# Testing Keyword Routing logic (mimicking app.py logic)
def test_keyword_routing_logic():
    def get_route(prompt):
        prompt_lower = prompt.lower()
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            return 'image'
        elif any(keyword in prompt_lower for keyword in ['музык', 'песн', 'трек']):
            return 'music'
        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            return 'video'
        else:
            return 'text'

    # Test Image Keywords
    assert get_route("Нарисуй мне кота") == 'image'
    assert get_route("Сделай фото леса") == 'image'
    assert get_route("Покажи изображение") == 'image'

    # Test Music Keywords
    assert get_route("Сгенерируй музыку") == 'music'
    assert get_route("Спой песню") == 'music'
    assert get_route("Новый трек") == 'music'
    assert get_route("Включи песню") == 'music' # morphological variation

    # Test Video Keywords
    assert get_route("Сделай видео") == 'video'
    assert get_route("Смешной ролик") == 'video'

    # Test Text Keywords (default)
    assert get_route("Как дела?") == 'text'
    assert get_route("Расскажи сказку") == 'text'
