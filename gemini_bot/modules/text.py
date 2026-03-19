from google import genai

class ChatSession:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        # Use gemini-2.0-flash as it's the latest and supports chats.
        self.chat = self.client.chats.create(model="gemini-2.0-flash")
        self.history = []  # Maintain UI history separately

    def get_history(self):
        return self.history

    def add_to_history(self, message: dict):
        self.history.append(message)

    def send_message_stream(self, prompt: str):
        """Sends a message to the model and streams the response."""
        try:
            response = self.chat.send_message_stream(prompt)
            for chunk in response:
                yield chunk.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate text response: {str(e)}")

def init_chat_session(api_key: str) -> ChatSession:
    return ChatSession(api_key)
