from gradio_client import Client
import os

def generate_video(prompt):
    """
    Generates video using ModelScope text-to-video via Hugging Face Spaces.
    Args:
        prompt (str): Description of the video.
    Returns:
        str: Path to the generated video file.
    """
    try:
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")

        # Parameters: prompt, seed (-1 random), num_frames (16), num_inference_steps (25)
        # Note: The specific arguments depend on the space's interface.
        result = client.predict(
            prompt,
            -1,
            16,
            25,
            api_name="/predict"
        )
        # The result is usually a dictionary or a path. In most video spaces, it returns a path to mp4.
        if isinstance(result, tuple) or isinstance(result, list):
            # Sometimes returns (video_path, json_info)
            return result[0]
        return result
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
