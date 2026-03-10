import google.generativeai as genai

def generate_text_stream(prompt, api_key, chat_history=None):
    if chat_history is None:
        chat_history = []

    genai.configure(api_key=api_key)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=chat_history)

        response = chat.send_message(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                yield chunk.text

        # Update chat history in place or return updated history
        chat_history.append({"role": "user", "parts": [prompt]})
        chat_history.append({"role": "model", "parts": [response.text]})

    except Exception as e:
        yield f"Произошла ошибка при генерации текста: {str(e)}"
