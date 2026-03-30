from gradio_client import Client

def init_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client: {e}"

def generate_video(prompt, client):
    try:
        result = client.predict(
            prompt,
            -1,  # seed
            16,  # num_frames
            25,  # num_inference_steps
            api_name="/video_synthesis"
        )
        # `result` is typically a dict with 'video' containing the file path
        if isinstance(result, dict) and 'video' in result:
             return result['video']
        return result
    except Exception as e:
        return f"Error generating video: {e}"
