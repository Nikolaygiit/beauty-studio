def generate_text_stream(prompt, history=None):
    import google.generativeai as genai

    if history is None:
        history = []

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Convert app history format to Gemini format
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(prompt, stream=True)

        for chunk in response:
            try:
                if chunk.text:
                    yield chunk.text
            except ValueError:
                yield "\n[Ошибка при получении части текста. Возможно блокировка контента.]"

    except Exception as e:
        yield f"\n\nПроизошла ошибка при генерации текста: {e}"