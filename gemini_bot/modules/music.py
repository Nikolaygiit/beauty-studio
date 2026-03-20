import random
from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        try:
            self.client = Client("sanchit-gandhi/musicgen-streaming")
            self.error = None
        except Exception as e:
            self.client = None
            self.error = f"Failed to initialize music client: {e}"

    def generate(self, prompt: str):
        if self.client is None:
            return None, self.error

        try:
            seed = random.randint(1, 100000)
            # Default parameters based on predict signature from memory
            audio_path = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=15,
                play_steps_in_s=1.5,
                seed=seed,
                api_name="/generate_audio"
            )
            return audio_path, None
        except Exception as e:
            return None, f"Error generating music: {e}"
