from gradio_client import Client

class VideoGenerator:
    def __init__(self):
        self.client = None
        self.error_msg = None
        try:
            self.client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        except Exception as e:
            # specifically handle RUNTIME_ERROR from damo-vilab gracefully
            self.error_msg = f"Ошибка инициализации генератора видео (модель может быть временно недоступна): {str(e)}"

    def generate_video(self, prompt):
        if self.error_msg:
            return self.error_msg

        try:
            result = self.client.predict(
                prompt,
                -1, # seed
                25, # num_inference_steps
                16, # num_frames
                api_name="/video_synthesis"
            )
            return result
        except Exception as e:
            return f"Произошла ошибка при генерации видео: {str(e)}"

def get_video_generator():
    return VideoGenerator()
