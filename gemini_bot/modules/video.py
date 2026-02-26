from gradio_client import Client

class VideoGenerator:
    def __init__(self):
        try:
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        except Exception as e:
            print(f"Error initializing VideoGenerator: {e}")
            self.client = None

    def generate_video(self, prompt):
        if not self.client:
            return None, "Video generator client not initialized."

        try:
            # The exact signature depends on the Space's API.
            # Usually it takes a text prompt.
            result = self.client.predict(
                prompt,	# str  in 'Input Text' Textbox component
                fn_index=0
            )
            return result
        except Exception as e:
            return None, f"Error generating video: {str(e)}"
