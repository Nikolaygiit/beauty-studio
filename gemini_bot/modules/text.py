import google.generativeai as genai

def get_gemini_response(prompt, chat_session=None):
    try:
        if chat_session is None:
            model = genai.GenerativeModel('gemini-1.5-flash')
            chat_session = model.start_chat(history=[])

        response = chat_session.send_message(prompt, stream=True)
        return response, chat_session
    except Exception as e:
        return f"An error occurred: {e}", chat_session
