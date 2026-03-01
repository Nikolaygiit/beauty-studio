from gradio_client import Client

def get_video_client():
    """Initializes and returns the Gradio client for video generation."""
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        print(f"Failed to initialize video client: {e}")
        return None

def generate_video(prompt: str, client: Client):
    """
    Generates video using Gradio client for modelscope-text-to-video-synthesis
    Fixed parameters: seed=-1, num_frames=16, num_inference_steps=25
    """
    if client is None:
        return "Error: Video client is not initialized."

    try:
        result = client.predict(
            prompt,	# str in 'Input Text' Textbox component
            -1,	# float (numeric value between -1 and 2147483647) in 'Seed' Slider component
            16,	# float (numeric value between 16 and 16) in 'Number of Frames' Slider component
            25,	# float (numeric value between 10 and 50) in 'Number of Inference Steps' Slider component
            fn_index=0
        )
        return result
    except Exception as e:
        return f"Error generating video: {str(e)}"
