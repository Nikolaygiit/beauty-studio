from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt):
    """
    Generates music using sanchit-gandhi/musicgen-streaming space.
    Returns (audio_path, error_message).
    """
    try:
        client = get_music_client()
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # `result` is a tuple. The first element is usually the filepath
        if isinstance(result, tuple) and len(result) > 0:
            return result[0], None
        return result, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
