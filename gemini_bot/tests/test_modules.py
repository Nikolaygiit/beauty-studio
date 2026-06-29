import pytest
from modules.text import get_gemini_client
from modules.image import generate_image
from modules.music import get_music_client, generate_music
from modules.video import get_video_client, generate_video

def test_get_gemini_client(mocker):
    # Mock genai.Client and its chat creation
    mock_client_class = mocker.patch('modules.text.genai.Client')
    mock_client_instance = mock_client_class.return_value
    mock_chat = mocker.Mock()
    mock_client_instance.chats.create.return_value = mock_chat

    chat, error = get_gemini_client('fake_api_key')

    assert chat is not None
    assert error == ""
    mock_client_class.assert_called_once_with(api_key='fake_api_key')
    mock_client_instance.chats.create.assert_called_once()

def test_get_gemini_client_error(mocker):
    # Mock genai.Client to raise an exception
    mock_client_class = mocker.patch('modules.text.genai.Client')
    mock_client_class.side_effect = Exception("API Key Invalid")

    chat, error = get_gemini_client('fake_api_key')

    assert chat is None
    assert "Ошибка инициализации Gemini: API Key Invalid" in error

def test_generate_image():
    # generate_image only constructs a URL and doesn't make an external call in our implementation
    url, error = generate_image("test prompt")

    assert "https://image.pollinations.ai/prompt/test%20prompt?seed=" in url
    assert error == ""

def test_get_music_client(mocker):
    # We clear the st.cache_resource cache for testing
    import streamlit as st
    st.cache_resource.clear()

    mock_client_class = mocker.patch('modules.music.Client')
    mock_client_instance = mocker.Mock()
    mock_client_class.return_value = mock_client_instance

    client, error = get_music_client()

    assert client is not None
    assert error == ""
    mock_client_class.assert_called_once_with("sanchit-gandhi/musicgen-streaming")

def test_generate_music(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mock_get_music_client = mocker.patch('modules.music.get_music_client')
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "/path/to/fake_audio.wav"
    mock_get_music_client.return_value = (mock_client, "")

    path, error = generate_music("test music")

    assert path == "/path/to/fake_audio.wav"
    assert error == ""
    mock_client.predict.assert_called_once_with(
        text_prompt="test music",
        audio_length_in_s=15,
        play_steps_in_s=1.5,
        seed=0,
        api_name="/generate_audio"
    )

def test_get_video_client(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mock_client_class = mocker.patch('modules.video.Client')
    mock_client_instance = mocker.Mock()
    mock_client_class.return_value = mock_client_instance

    client, error = get_video_client()

    assert client is not None
    assert error == ""
    mock_client_class.assert_called_once_with("damo-vilab/modelscope-text-to-video-synthesis")

def test_generate_video(mocker):
    import streamlit as st
    st.cache_resource.clear()

    mock_get_video_client = mocker.patch('modules.video.get_video_client')
    mock_client = mocker.Mock()
    mock_client.predict.return_value = "/path/to/fake_video.mp4"
    mock_get_video_client.return_value = (mock_client, "")

    path, error = generate_video("test video")

    assert path == "/path/to/fake_video.mp4"
    assert error == ""
    mock_client.predict.assert_called_once_with(
        "test video",
        -1,
        16,
        25,
        api_name="/generate_video"
    )
