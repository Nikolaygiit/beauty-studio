from gradio_client import Client

def generate_video(prompt):
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/generate_video"
        )
        # result is typically a tuple containing the path to the video
        video_path = result[0] if isinstance(result, tuple) else result
        return video_path, None
    except Exception as e:
        return None, f"Ошибка генерации видео: {str(e)}"
