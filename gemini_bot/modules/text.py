import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiHandler:
    def __init__(self, model_name="gemini-1.5-flash", api_key=None, system_instruction=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Please set it in .env or the sidebar.")

        genai.configure(api_key=self.api_key)

        self.model_name = model_name
        self.system_instruction = system_instruction

        # Initialize model with system instruction if provided
        if self.system_instruction:
             self.model = genai.GenerativeModel(model_name, system_instruction=self.system_instruction)
        else:
             self.model = genai.GenerativeModel(model_name)

        self.chat = None

    def start_chat(self, history=None):
        """Starts a chat session."""
        self.chat = self.model.start_chat(history=history or [])
        return self.chat

    def send_message(self, content, stream=True):
        """
        Sends a message to the chat session.
        Content can be text (str) or a list including images (PIL.Image).
        """
        if not self.chat:
            self.start_chat()

        try:
            response = self.chat.send_message(content, stream=stream)
            return response
        except Exception as e:
            # Propagate exception so app.py can handle it appropriately
            raise e

    @staticmethod
    def list_models():
        """Lists available Gemini models."""
        try:
            return [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            return ["models/gemini-1.5-flash", "models/gemini-1.5-pro"]
