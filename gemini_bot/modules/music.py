from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        try:
            # Space for streaming musicgen
            self.client = Client("sanchit-gandhi/musicgen-streaming")
            self.error = None
        except Exception as e:
            self.client = None
            self.error = f"Ошибка инициализации музыкальной модели: {str(e)}"

    def generate(self, prompt: str) -> str:
        """
        Генерирует музыку по текстовому запросу и возвращает путь к аудиофайлу.
        """
        if self.client is None:
            return self.error

        try:
            # API expects: text_prompt, audio_length_in_s, play_steps_in_s, seed
            # We'll use 15 seconds as a nice default
            result = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=15,
                play_steps_in_s=1.5,
                seed=5,
                api_name="/generate_audio"
            )
            # The result is typically the path to the generated audio
            return result
        except Exception as e:
            return f"Произошла ошибка при генерации музыки: {str(e)}"

def get_music_generator():
    return MusicGenerator()
