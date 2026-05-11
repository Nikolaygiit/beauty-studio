import os
from gradio_client import Client

def generate_music(prompt):
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")

        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )

        # result is typically a tuple of (audio_path, ...), Gradio sometimes returns a single path string or a tuple
        # based on memory instructions, client.predict usually returns the path directly or a tuple where first elem is path
        audio_path = result[0] if isinstance(result, tuple) else result

        return audio_path, None
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {str(e)}"
