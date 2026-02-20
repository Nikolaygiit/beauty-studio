from gradio_client import Client
import os

def generate_video(prompt, hf_token=None):
    """
    Generates video using DAMO text-to-video Space.

    Args:
        prompt (str): Description of the video.
        hf_token (str): Optional Hugging Face token.

    Returns:
        str: Path to the generated video file, or None on failure.
    """
    try:
        # Check if HF_TOKEN is in environment if not provided
        if not hf_token:
            hf_token = os.getenv("HF_TOKEN")

        client = Client("damo-vilab/modelscope-damo-text-to-video-synthesis", hf_token=hf_token)
        result = client.predict(
            prompt,
            -1, # Seed (-1 for random)
            16, # Number of frames
            25, # Number of inference steps
            api_name="/predict"
        )
        return result
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
