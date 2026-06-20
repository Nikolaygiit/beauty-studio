from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video
from modules.text import create_client_and_chat, generate_text_stream

def test_generate_image_url():
    url = generate_image_url("кот")
    assert "https://image.pollinations.ai/prompt/" in url
    assert "кот" not in url # it should be url encoded
    assert "%D0%BA%D0%BE%D1%82" in url
    assert "seed=" in url

def test_generate_music_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = ("mock_audio.wav",)

    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    path, error = generate_music("rock song")
    assert path == "mock_audio.wav"
    assert error is None
    mock_client.predict.assert_called_once()

def test_generate_music_error(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.side_effect = Exception("API error")

    mocker.patch("modules.music.get_music_client", return_value=mock_client)

    path, error = generate_music("rock song")
    assert path is None
    assert "Ошибка при генерации музыки: API error" in error

def test_generate_video_success(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.return_value = "mock_video.mp4"

    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    path, error = generate_video("cat video")
    assert path == "mock_video.mp4"
    assert error is None
    mock_client.predict.assert_called_once()

def test_generate_video_error(mocker):
    mock_client = mocker.MagicMock()
    mock_client.predict.side_effect = Exception("API error")

    mocker.patch("modules.video.get_video_client", return_value=mock_client)

    path, error = generate_video("cat video")
    assert path is None
    assert "Ошибка при генерации видео: API error" in error

def test_create_client_and_chat_error(mocker):
    mocker.patch("modules.text.genai.Client", side_effect=Exception("Invalid API Key"))
    client, chat = create_client_and_chat("bad_key")
    assert client is None
    assert chat is None

def test_generate_text_stream():
    # Mocking a chat session that yields chunks
    class MockChunk:
        def __init__(self, text):
            self.text = text

    class MockChatSession:
        def send_message_stream(self, prompt):
            yield MockChunk("Привет")
            yield MockChunk(", ")
            yield MockChunk("мир!")

    chat = MockChatSession()
    chunks = list(generate_text_stream(chat, "test"))
    assert chunks == ["Привет", ", ", "мир!"]

def test_generate_text_stream_error():
    class MockChatSession:
        def send_message_stream(self, prompt):
            raise Exception("Network error")

    chat = MockChatSession()
    chunks = list(generate_text_stream(chat, "test"))
    assert len(chunks) == 1
    assert "Произошла ошибка при генерации текста: Network error" in chunks[0]
