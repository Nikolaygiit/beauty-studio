import google.generativeai as genai

def get_chat_session(api_key, history=None):
    if history is None:
        history = []
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=history)
    return chat

def generate_text_stream(chat, prompt):
    try:
        response = chat.send_message(prompt, stream=True)
        for chunk in response:
            yield chunk.text
    except Exception as e:
        yield f"\n[Ошибка генерации текста: {e}]"
