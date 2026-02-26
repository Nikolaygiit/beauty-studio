from gradio_client import Client

class MusicGenerator:
    def __init__(self):
        try:
            self.client = Client("sanchit-gandhi/musicgen-streaming")
        except Exception as e:
            print(f"Error initializing MusicGenerator: {e}")
            self.client = None

    def generate_music(self, prompt, duration=10):
        if not self.client:
            return None, "Music generator client not initialized."

        try:
            # The exact signature depends on the Space's API.
            # Usually it takes a text prompt.
            # Assuming standard predict call.
            result = self.client.predict(
                prompt,	# str  in 'Input Text' Textbox component
                fn_index=0
            )
            return result
        except Exception as e:
            return None, f"Error generating music: {str(e)}"
