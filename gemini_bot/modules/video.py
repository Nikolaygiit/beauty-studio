from gradio_client import Client

class VideoGenerator:
    def __init__(self):
        try:
            # Note: space may be in RUNTIME_ERROR as tested earlier, handle gracefully
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
            self.error = None
        except Exception as e:
            self.client = None
            self.error = f"The model is currently unavailable (e.g., RUNTIME_ERROR). Detailed error: {str(e)}"

    def generate(self, prompt: str) -> str:
        """
        Генерирует видео по текстовому запросу и возвращает путь к видеофайлу.
        """
        if self.client is None:
            return self.error

        try:
            result = self.client.predict(
                prompt=prompt,
                seed=-1,
                num_frames=16,
                num_inference_steps=25,
                api_name="/predict"
            )
            return result
        except Exception as e:
            return f"Произошла ошибка при генерации видео: {str(e)}"

def get_video_generator():
    return VideoGenerator()
