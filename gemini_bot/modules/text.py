import google.generativeai as genai
import os

def configure_api(api_key):
    """Configures the Google Generative AI API."""
    if api_key:
        genai.configure(api_key=api_key)

def generate_response(prompt, history=None, model_name="gemini-1.5-flash"):
    """
    Generates a response from the model using chat history.

    Args:
        prompt (str): The user's input.
        history (list): The chat history in Streamlit format [{'role': 'user', 'content': '...'}, ...].
        model_name (str): The name of the model to use.

    Returns:
        generator: A stream of response chunks (strings).
    """
    try:
        model = genai.GenerativeModel(model_name)

        formatted_history = []
        if history:
            for msg in history:
                # Filter out messages that might not be text or have invalid roles if necessary
                if msg.get("role") in ["user", "assistant"] and msg.get("content"):
                    role = "user" if msg["role"] == "user" else "model"
                    formatted_history.append({"role": role, "parts": [msg["content"]]})

        chat = model.start_chat(history=formatted_history)
        response = chat.send_message(prompt, stream=True)

        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Error generating text: {str(e)}"
