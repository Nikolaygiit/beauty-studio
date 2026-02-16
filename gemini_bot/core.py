import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiHandler:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Please set GOOGLE_API_KEY in .env or provide it.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_content(self, prompt, image=None):
        """
        Generates content using Gemini model.

        Args:
            prompt (str): The text prompt.
            image (PIL.Image or list, optional): Image(s) to include in the prompt.

        Returns:
            str: The generated text response.
        """
        try:
            if image:
                if isinstance(image, list):
                    inputs = [prompt] + image
                else:
                    inputs = [prompt, image]
                response = self.model.generate_content(inputs)
            else:
                response = self.model.generate_content(prompt)

            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

    def chat(self, history, prompt, image=None):
        """
        Handles chat interaction.
        This is a simplified chat handler. For persistent chat, we might need to manage history manually
        or use start_chat.
        """
        # For this simple bot, we will just use generate_content as it is stateless,
        # but Streamlit will manage the history in the UI.
        # If we wanted multi-turn with memory, we'd use start_chat.
        # But since streamlit re-runs, passing history as context in prompt is often easier or
        # using the chat object but persisting it in session_state.

        # Let's try to use the chat session if possible, but for "turnkey" simple usage,
        # passing the whole context might be better or just rely on the model's single turn.

        # For now, let's stick to single turn or simple context management in UI.
        return self.generate_content(prompt, image)
