from gradio_client import Client
import tempfile
import shutil
import os

class MusicGenerator:
    def __init__(self):
        try:
            self.client = Client("sanchit-gandhi/musicgen-streaming")
        except Exception as e:
            print(f"Error initializing MusicGen client: {e}")
            self.client = None

    def generate(self, prompt: str, length: int) -> str:
        if not self.client:
            return "❌ MusicGen client failed to initialize."

        try:
            # According to Gradio Client API view:
            # predict(text_prompt, audio_length_in_s, play_steps_in_s, seed, api_name="/generate_audio") -> generated_music
            result_path = self.client.predict(
                text_prompt=prompt,
                audio_length_in_s=length,
                play_steps_in_s=1.5,
                seed=5,
                api_name="/generate_audio"
            )

            # Gradio often returns a temporary path. We should copy it to a more stable location if needed
            if result_path and os.path.exists(result_path):
                # Copying to avoid temp file deletion issues
                temp_dir = tempfile.gettempdir()
                dest_path = os.path.join(temp_dir, f"generated_music_{hash(prompt)}.wav")
                shutil.copy2(result_path, dest_path)
                return dest_path

            return result_path

        except Exception as e:
            raise Exception(f"Failed to generate music: {str(e)}")
