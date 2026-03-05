import google.generativeai as genai

class TextGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_response(self, user_input: str, history: list) -> str:
        # Create a new chat session with the given history
        chat = self.model.start_chat(history=history)

        try:
            # Send message and get response
            response = chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"❌ Ошибка генерации текста: {e}"
