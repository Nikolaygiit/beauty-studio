from gradio_client import Client

def get_video_generator():
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        return client
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Video generation service is currently unavailable."
        return f"Error initializing video generator: {str(e)}"

def generate_video(client, prompt):
    if isinstance(client, str):
        return client # Error message
    try:
        # fixed parameters: seed=-1, num_frames=16, and num_inference_steps=25
        result = client.predict(
            prompt,
            -1, # seed
            16, # num_frames
            25, # num_inference_steps
            api_name="/video_synthesis"
        )
        return result
    except Exception as e:
        if "RUNTIME_ERROR" in str(e):
            return "Video generation service is currently unavailable. Please try again later."
        return f"Error generating video: {str(e)}"
