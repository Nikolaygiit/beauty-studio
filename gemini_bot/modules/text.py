import google.generativeai as genai
import streamlit as st

class GeminiText:
    def __init__(self, api_key):
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.chat = self.model.start_chat(history=[])
        else:
            self.model = None
            self.chat = None

    def send_message(self, prompt):
        if not self.model:
            return "Please enter your Google API Key in the sidebar."

        try:
            response = self.chat.send_message(prompt, stream=True)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

    def get_history(self):
        if self.chat:
            return self.chat.history
        return []
