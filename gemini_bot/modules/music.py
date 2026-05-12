import os
from gradio_client import Client

def generate_music(prompt):
    """
    Generates music using the sanchit-gandhi/musicgen-streaming Gradio space.
    Returns (audio_path, None) on success, or (None, error_message) on failure.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        result = client.predict(
            text_prompt=prompt,
            audio_length_in_s=15,
            play_steps_in_s=1.5,
            seed=0,
            api_name="/generate_audio"
        )
        # The result might be a tuple/list depending on the space's exact return,
        # typically the first element is the filepath for the generated audio.
        if isinstance(result, tuple) or isinstance(result, list):
            audio_path = result[0]
        else:
            audio_path = result

        if audio_path and os.path.exists(audio_path):
            return audio_path, None
        else:
            return None, "Аудиофайл не был сгенерирован или не найден."
    except Exception as e:
        return None, f"Ошибка при генерации музыки: {e}"
