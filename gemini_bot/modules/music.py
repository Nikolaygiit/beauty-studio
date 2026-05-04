from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt):
    """
    Generates music based on the prompt using the sanchit-gandhi/musicgen-streaming space.
    """
    client = get_music_client()
    if not client:
         return None, "Не удалось инициализировать клиент для генерации музыки."

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        return result, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
