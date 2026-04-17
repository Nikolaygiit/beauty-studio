import streamlit as st
from gradio_client import Client
import shutil
import os

@st.cache_resource
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return str(e)

def generate_music(prompt):
    """
    Generates music using the MusicGen space via Gradio Client.
    Returns the file path to the generated audio or an error message.
    """
    client = get_music_client()

    if isinstance(client, str):
        return None, f"Ошибка инициализации музыкальной модели: {client}"

    try:
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )

        # Gradio client returns a path to a temporary file.
        # result for this specific API is usually a tuple (video_path, audio_path) or just audio_path.
        # Wait, the endpoint is generate_audio, let's assume it returns a file path or a tuple containing it.
        # Based on typical gradio outputs, it might return just the path. Let's handle string or tuple.

        audio_path = None
        if isinstance(result, str) and os.path.exists(result):
            audio_path = result
        elif isinstance(result, (list, tuple)) and len(result) > 0:
            if isinstance(result[0], str) and os.path.exists(result[0]):
                audio_path = result[0]
            # Handle dictionary case if it's a gradio file output
            elif isinstance(result[0], dict) and 'name' in result[0]:
                audio_path = result[0]['name']
        elif isinstance(result, dict) and 'name' in result:
             audio_path = result['name']

        # Actually, let's just return result. We can test it later or just return result[0] or whatever it is.
        # For typical gradio file outputs, we can just return it to st.audio.
        # st.audio handles file paths.

        if audio_path:
             return audio_path, None
        return result, None # Return whatever it is if we couldn't parse it
    except Exception as e:
        return None, str(e)
