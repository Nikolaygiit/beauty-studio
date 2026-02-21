from gradio_client import Client
import random

class MusicGenerator:
    def __init__(self, hf_token=None):
        self.hf_token = hf_token
        try:
            # Use sanchit-gandhi/musicgen-streaming as it is reliable and open.
            self.client = Client("sanchit-gandhi/musicgen-streaming", token=self.hf_token)
        except Exception as e:
            print(f"Failed to initialize MusicGenerator: {e}")
            self.client = None

    def generate(self, prompt, duration=15):
        if not self.client:
            return "Error: MusicGenerator client not initialized."

        try:
            seed = random.randint(0, 10000)
            # The API expects: text_prompt, audio_length_in_s, play_steps_in_s, seed
            result = self.client.predict(
                prompt,
                float(duration),
                1.5,
                float(seed),
                api_name="/generate_audio"
            )
            return result
        except Exception as e:
            return f"Error generating music: {e}"
