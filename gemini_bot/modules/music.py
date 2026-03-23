from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        self.client = None
        self.error_msg = None
        try:
            self.client = Client("sanchit-gandhi/musicgen-streaming")
        except Exception as e:
            self.error_msg = f"Ошибка инициализации генератора музыки: {str(e)}"

    def generate_music(self, prompt):
        if self.error_msg:
            return self.error_msg

        try:
            result = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=15,
                play_steps_in_s=1.5,
                seed=5,
                api_name="/generate_audio"
            )
            # The result is a tuple if there are multiple outputs, or single string.
            # In musicgen, it usually streams to a tuple or returns a path.
            # Client.predict on a stream returns a tuple or string path to audio file.
            return result
        except Exception as e:
            return f"Произошла ошибка при генерации музыки: {str(e)}"

def get_music_generator():
    return MusicGenerator()
