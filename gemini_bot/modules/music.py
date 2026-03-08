from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        self.client = None

    def initialize(self):
        if self.client is None:
            try:
                self.client = Client("sanchit-gandhi/musicgen-streaming")
            except Exception as e:
                return f"Ошибка инициализации генератора музыки: {str(e)}"
        return None

    def generate(self, prompt, audio_length_in_s=15, play_steps_in_s=1.5, seed=5):
        init_error = self.initialize()
        if init_error:
            return None, init_error

        try:
            result = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=audio_length_in_s,
                play_steps_in_s=play_steps_in_s,
                seed=seed,
                api_name="/generate_audio"
            )
            return result, None
        except Exception as e:
            return None, f"Ошибка при генерации музыки: {str(e)}"
