import google.generativeai as genai
import os

class TextGeneration:
    def __init__(self, api_key, model_name="gemini-1.5-flash"):
        self.api_key = api_key
        if not api_key:
            raise ValueError("API Key is required")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message, stream=True):
        """
        Sends a message to the Gemini model.
        Args:
            message (str): The user's message.
            stream (bool): Whether to stream the response.
        Returns:
            The response object (iterable if stream=True).
        """
        try:
            response = self.chat.send_message(message, stream=stream)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        return self.chat.history

    def clear_history(self):
        self.chat = self.model.start_chat(history=[])
