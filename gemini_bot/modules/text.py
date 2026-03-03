import google.generativeai as genai

def init_gemini(api_key):
    """Initializes the Gemini model with the provided API key."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

def generate_text_stream(model, prompt, history=[]):
    """
    Generates text streaming from Gemini model using history.
    history is a list of dictionaries with 'role' and 'parts'.
    Returns a generator yielding text chunks.
    """
    try:
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации ответа: {str(e)}"
