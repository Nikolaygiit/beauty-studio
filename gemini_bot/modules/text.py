import google.generativeai as genai
import os

class TextGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        if not api_key:
            raise ValueError("API Key is required")
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat_session = None
        except Exception as e:
            raise ValueError(f"Failed to configure Gemini: {e}")

    def start_chat(self, history=None):
        if history is None:
            history = []
        self.chat_session = self.model.start_chat(history=history)

    def send_message(self, message):
        if not self.chat_session:
            self.start_chat()
        try:
            response = self.chat_session.send_message(message)
            return response.text
        except Exception as e:
            return f"Error: {e}"

    def get_history(self):
        if self.chat_session:
            return self.chat_session.history
        return []
