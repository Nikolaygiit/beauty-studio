import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def generate_music(prompt: str) -> tuple[str | None, str | None]:
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio Space.
    Returns (audio_path, error_msg).
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
        # `result` is typically a tuple or string (path to file).
        # We need the path to the audio file. For this client, the second output is often the full audio path.
        if isinstance(result, tuple) and len(result) > 1:
             audio_path = result[1]
        elif isinstance(result, str):
            audio_path = result
        else:
             audio_path = str(result)
        return audio_path, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
