import logging
from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        self.client = None
        self.error_state = None
        try:
            self.client = Client("sanchit-gandhi/musicgen-streaming")
        except Exception as e:
            self.error_state = str(e)
            logging.error(f"Failed to initialize MusicGenerator: {e}")

    def generate(self, prompt: str, length_s: float = 15.0, play_steps_s: float = 1.5, seed: float = 5.0) -> str:
        """
        Generates music based on a text prompt.
        Returns the path to the generated audio file or an error message.
        """
        if self.error_state:
            return f"Ошибка инициализации музыкального генератора: {self.error_state}"

        try:
            # Note: gradio_client may return a tuple or string depending on space,
            # but usually it's a file path string for audio.
            result = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=length_s,
                play_steps_in_s=play_steps_s,
                seed=seed,
                api_name="/generate_audio"
            )
            return result
        except Exception as e:
            error_msg = f"Ошибка генерации музыки: {str(e)}"
            logging.error(error_msg)
            return error_msg
