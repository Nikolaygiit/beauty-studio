import os
from gradio_client import Client

def get_music_client():
    """Initializes and returns the Gradio client for the music generation model."""
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        return None

def generate_music(client, prompt):
    """
    Generates music based on the prompt using the initialized client.
    Returns the path to the downloaded audio file or an error message.
    """
    if client is None:
        return None, "Music generation client could not be initialized."

    try:
        # MusicGen client fn_index 0 typically returns:
        # Tuple[str(audio_path), str(video_path)]
        # We'll just grab the result and figure out the path.
        result = client.predict(
            text=prompt,
            melody=None,
            fn_index=0
        )

        # Result from sanchit-gandhi/musicgen-streaming typically is a tuple
        # (audio_file_path, something_else) or just audio path.
        if isinstance(result, tuple):
            audio_path = result[0]
        else:
            audio_path = result

        return audio_path, None
    except Exception as e:
        return None, f"Ошибка генерации музыки: {str(e)}"
