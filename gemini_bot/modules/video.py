from gradio_client import Client
import shutil
import os
import time

def generate_video(prompt, output_dir="gemini_bot/assets"):
    """
    Generates video using Gradio Client.

    Args:
        prompt (str): The prompt for video generation.
        output_dir (str): Directory to save the generated file.

    Returns:
        str: Path to the generated video file.
    """
    try:
        # damo-vilab/modelscope-text-to-video-synthesis is often busy or down.
        # We try to connect.
        client = Client("damo-vilab/modelscope-text-to-video-synthesis")

        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        result = client.predict(
                prompt,
                -1, # seed
                16, # num frames
                25, # num steps
                api_name="/predict"
        )

        # result is a filepath
        original_path = result
        # It's usually .mp4
        file_extension = os.path.splitext(original_path)[1]
        if not file_extension:
             file_extension = ".mp4"

        filename = f"video_{int(time.time())}{file_extension}"
        destination_path = os.path.join(output_dir, filename)

        shutil.copy(original_path, destination_path)
        return destination_path

    except Exception as e:
        return f"Error generating video: {str(e)}"
