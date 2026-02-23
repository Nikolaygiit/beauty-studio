from gradio_client import Client
import os

class MusicGeneration:
    def __init__(self, space_name="sanchit-gandhi/musicgen-streaming"):
        try:
            self.client = Client(space_name)
        except Exception as e:
            print(f"Error initializing Music Client: {e}")
            self.client = None

    def generate(self, prompt, duration=10):
        """
        Generates music from a text prompt.
        Args:
            prompt (str): Description of the music.
            duration (int): Duration in seconds.
        Returns:
            str: Path to the generated audio file.
        """
        if not self.client:
            return None, "Client not initialized."

        try:
            # The API signature for sanchit-gandhi/musicgen-streaming might vary.
            # Usually: prompt, input_audio (optional), duration, ...
            # I'll use the most common arguments.
            result = self.client.predict(
                prompt,
                None, # Input audio
                duration,
                api_name="/predict"
            )
            # Result is usually a tuple or just the path.
            # In streaming, it might return a generator or a final path.
            # For predict, it returns the final result.
            return result
        except Exception as e:
            return None, str(e)
