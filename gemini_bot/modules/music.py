from gradio_client import Client
import shutil
import os
import time

def generate_music(prompt, output_dir="gemini_bot/assets"):
    """
    Generates music using Gradio Client.

    Args:
        prompt (str): The prompt for music generation.
        output_dir (str): Directory to save the generated file.

    Returns:
        str: Path to the generated audio file.
    """
    try:
        client = Client("sanchit-gandhi/musicgen-streaming")
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        result = client.predict(
                prompt,	# str  in 'Input Text' Textbox component
                15,	# float  in 'Duration (seconds)' Slider component
                1.5,	# float  in 'Play Steps (seconds)' Slider component
                5,	# float  in 'Seed' Slider component
                api_name="/generate_audio"
        )

        # Result is a filepath
        original_path = result
        file_extension = os.path.splitext(original_path)[1]
        if not file_extension:
             file_extension = ".wav" # Default to wav if unknown

        filename = f"music_{int(time.time())}{file_extension}"
        destination_path = os.path.join(output_dir, filename)

        shutil.copy(original_path, destination_path)
        return destination_path

    except Exception as e:
        return f"Error generating music: {str(e)}"
