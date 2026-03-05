from gradio_client import Client
import os
import shutil
import tempfile

class VideoGenerator:
    def __init__(self):
        try:
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        except Exception as e:
            print(f"Error initializing VideoGen client: {e}")
            self.client = None

    def generate(self, prompt: str) -> str:
        if not self.client:
            return "❌ VideoGen client failed to initialize."

        try:
            # Note: The 'damo-vilab/modelscope-text-to-video-synthesis' space often experiences runtime errors
            # due to high load or insufficient resources on HuggingFace.
            # We still try to call the predict API.
            # Based on memory, the video generation module is configured with fixed parameters: seed -1, 16 frames, and 25 inference steps.

            # Since the API is not working right now, we use a placeholder response if the client fails
            result_path = self.client.predict(
                prompt,	# str in 'parameter_11' Textbox component
                -1,	# float (numeric value between -1 and 2147483647) in 'Seed' Slider component
                25,	# float (numeric value between 10 and 50) in 'Number of inference steps' Slider component
                16,	# float (numeric value between 8 and 32) in 'Number of frames' Slider component
                api_name="/predict"
            )

            if result_path and os.path.exists(result_path):
                # Copying to avoid temp file deletion issues
                temp_dir = tempfile.gettempdir()
                dest_path = os.path.join(temp_dir, f"generated_video_{hash(prompt)}.mp4")
                shutil.copy2(result_path, dest_path)
                return dest_path

            return result_path

        except Exception as e:
            raise Exception(f"Failed to generate video: {str(e)}\n\nThe ModelScope Text-to-Video space may be temporarily unavailable or in an invalid state.")
