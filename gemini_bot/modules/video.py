import logging
from gradio_client import Client

class VideoGenerator:
    def __init__(self):
        self.client = None
        self.error_state = None
        try:
            # We attempt to initialize the client.
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        except Exception as e:
            # Catch RUNTIME_ERROR or other initialization errors
            self.error_state = f"Ошибка инициализации генератора видео: {str(e)}"
            logging.error(self.error_state)

    def generate(self, prompt: str) -> str:
        """
        Generates video based on a text prompt using fixed parameters.
        Returns the path to the generated video file or an error message.
        Fixed parameters: seed -1, 16 frames, 25 inference steps.
        """
        if self.error_state:
            return self.error_state

        try:
            result = self.client.predict(
                prompt=prompt,
                seed=-1,
                num_frames=16,
                num_inference_steps=25,
                api_name="/predict"
            )
            # Typically returns a dictionary containing 'video' filepath or just the filepath string
            # Let's extract the path properly if it's a dict or list
            if isinstance(result, dict) and 'video' in result:
                return result['video']
            elif isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and 'video' in result[0]:
                 return result[0]['video']
            elif isinstance(result, str):
                return result
            else:
                 # fallback for new API structures
                 return result
        except Exception as e:
            error_msg = f"Ошибка генерации видео: {str(e)}"
            logging.error(error_msg)
            return error_msg
