from modules.text import get_gemini_client, create_chat_session, generate_text_stream

def test_get_gemini_client_invalid_key():
    client, error = get_gemini_client("invalid_key")
    # Even with an invalid key, google-genai might initialize the client object,
    # but let's check that it doesn't crash.
    assert client is not None

class DummyChunk:
    def __init__(self, text):
        self.text = text

class DummyResponseStream:
    def __iter__(self):
        yield DummyChunk("Hello ")
        yield DummyChunk("World!")

class DummyChatSession:
    def send_message_stream(self, prompt):
         return DummyResponseStream()

def test_generate_text_stream():
    chat_session = DummyChatSession()
    response, error = generate_text_stream(chat_session, "Test prompt")
    assert error is None

    full_text = ""
    for chunk in response:
         if chunk.text:
              full_text += chunk.text

    assert full_text == "Hello World!"
