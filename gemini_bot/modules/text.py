def generate_text(prompt, chat_session):
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Произошла ошибка при генерации текста: {e}"
