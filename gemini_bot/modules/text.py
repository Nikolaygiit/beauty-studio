import google.generativeai as genai

def generate_text(prompt, api_key, history=None):
    """
    Generates text using Gemini 1.5 Flash.

    Args:
        prompt (str): The user's input prompt.
        api_key (str): The Google API Key.
        history (list): The chat history in Gemini format.

    Returns:
        tuple: (response_text, updated_history)
    """
    if history is None:
        history = []

    if not api_key:
        return "Error: API Key is missing.", history

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        chat = model.start_chat(history=history)
        response = chat.send_message(prompt)
        return response.text, chat.history
    except Exception as e:
        return f"Error generating text: {e}", history
