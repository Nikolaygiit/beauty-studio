import google.generativeai as genai

def get_gemini_model() -> genai.GenerativeModel:
    """
    Returns the gemini-1.5-flash GenerativeModel.
    """
    return genai.GenerativeModel('gemini-1.5-flash')

def generate_text_stream(chat_session, prompt: str):
    """
    Sends a message to the chat session and returns an iterator of text chunks.
    Handles general exceptions during the API call (e.g., blocked content).
    """
    try:
        response = chat_session.send_message(prompt, stream=True)
        return response
    except Exception as e:
        # Instead of failing silently, return a dummy generator yielding the error.
        def error_generator():
            yield f"Error occurred: {str(e)}"
        return error_generator()
