from gradio_client import Client
import os
import random

class VideoGenerator:
    def __init__(self, hf_token=None):
        self.hf_token = hf_token
        # Default to a known space, even if currently unstable
        self.space_name = os.getenv("VIDEO_SPACE_NAME", "damo-vilab/modelscope-text-to-video-synthesis")
        try:
            self.client = Client(self.space_name, token=self.hf_token)
        except Exception as e:
            print(f"Failed to initialize VideoGenerator with space {self.space_name}: {e}")
            self.client = None

    def generate(self, prompt):
        if not self.client:
            return "Error: VideoGenerator client not initialized. The Hugging Face Space might be down or private."

        try:
            # Attempt to generate video.
            # Note: Input arguments depend on the specific space implementation.
            # For damo-vilab/modelscope-text-to-video-synthesis, it typically expects a prompt.
            result = self.client.predict(
                prompt,
                api_name="/predict"
            )
            return result
        except Exception as e:
            return f"Error generating video: {e}"
