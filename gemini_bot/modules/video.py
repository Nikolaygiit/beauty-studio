from gradio_client import Client

class VideoGenerator:
    def __init__(self):
        try:
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
            self.error = None
        except Exception as e:
            self.client = None
            self.error = f"Failed to initialize video client: {e}"

    def generate(self, prompt: str):
        if self.client is None:
            return None, self.error

        try:
            # Memory says: fixed parameters: seed -1, 16 frames, and 25 inference steps
            video_path = self.client.predict(
                prompt, # str in 'prompt' Textbox component
                -1, # float in 'seed' Slider component
                25, # float in 'num_inference_steps' Slider component
                16, # float in 'num_frames' Slider component
                api_name="/text2video"
            )
            return video_path, None
        except Exception as e:
            return None, f"Error generating video: {e}"
