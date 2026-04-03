from gradio_client import Client

def get_video_client():
    """Initializes the video generation client."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        return f"Error initializing video client: {e}"

def generate_video(client, prompt):
    """Generates video based on the prompt."""
    try:
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/predict"
        )
        # The result typically contains a path to the generated video file
        return result
    except Exception as e:
        return f"Error generating video: {e}"
