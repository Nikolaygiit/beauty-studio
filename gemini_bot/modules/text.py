import google.generativeai as genai

def generate_text_stream(prompt, api_key, history=None):
    if history is None:
        history = []

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"\n\nПроизошла ошибка: {str(e)}"
