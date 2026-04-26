from gradio_client import Client
import streamlit as st

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(prompt):
    """Generates music using the musicgen-streaming space."""
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
        # The result might be a tuple or a dictionary depending on Gradio version and space output.
        # Usually, it's a tuple where the first element is the path to the audio file.
        if isinstance(result, tuple) and len(result) > 0:
             return result[0], None
        elif isinstance(result, str):
            return result, None
        elif isinstance(result, dict) and 'video' in result: # Sometimes audio spaces return video wrapper
            return result['video'], None
        elif isinstance(result, dict) and 'audio' in result:
             return result['audio'], None
        return result, None

    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
