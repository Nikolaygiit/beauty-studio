from gradio_client import Client

class VideoGeneration:
    def __init__(self, space_name="damo-vilab/modelscope-text-to-video-synthesis"):
        try:
            self.client = Client(space_name)
        except Exception as e:
            print(f"Error initializing Video Client: {e}")
            self.client = None

    def generate(self, prompt, seed=-1, num_frames=16, num_steps=25):
        """
        Generates video from a text prompt.
        Args:
            prompt (str): Description of the video.
        Returns:
            str: Path to the generated video file.
        """
        if not self.client:
            return None, "Client not initialized."

        try:
            # Common arguments for modelscope text-to-video
            result = self.client.predict(
                prompt,
                seed,
                num_frames,
                num_steps,
                api_name="/infer" # Sometimes it's /infer or /predict
            )
            # If /infer fails, we might try /predict, but usually spaces have one main endpoint.
            # Modelscope usually uses /infer or just calling the fn_index=0

            # Note: result is usually a path to the temporary video file.
            return result
        except Exception as e:
            # Fallback attempt? Usually not worth it blindly.
            return None, str(e)
