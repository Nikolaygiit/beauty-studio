from gradio_client import Client
import time

class VideoGenerator:
    def __init__(self):
        self.client = None

    def initialize(self):
        if self.client is None:
            try:
                self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
            except ValueError as e:
                if "RUNTIME_ERROR" in str(e):
                    return "Видео-модель сейчас недоступна (RUNTIME_ERROR). Попробуйте позже."
                return f"Ошибка инициализации генератора видео: {str(e)}"
            except Exception as e:
                return f"Ошибка инициализации генератора видео: {str(e)}"
        return None

    def generate(self, prompt, num_frames=16, num_inference_steps=25, seed=-1):
        init_error = self.initialize()
        if init_error:
            return None, init_error

        try:
            # We assume api_name predicts the video with these args
            # The original memory context said we should use fixed parameters (-1, 16, 25).
            result = self.client.predict(
                prompt, # str in 'text' Textbox component
                num_frames, # int | float (numeric value between 16 and 16) in 'Max Frames' Slider component
                num_inference_steps, # int | float (numeric value between 10 and 50) in 'Steps' Slider component
                seed, # int | float in 'Seed' Number component
                api_name="/predict"
            )

            # predict returns a string of the path to the video file.
            return result, None
        except ValueError as e:
            if "RUNTIME_ERROR" in str(e):
                 return None, "Видео-модель сейчас недоступна (RUNTIME_ERROR). Попробуйте позже."
            return None, f"Ошибка при генерации видео: {str(e)}"
        except Exception as e:
            return None, f"Ошибка при генерации видео: {str(e)}"
