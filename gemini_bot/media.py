import requests
from gradio_client import Client
import os
import time

def generate_image(prompt):
    """
    Generates an image using Pollinations.ai.
    Returns the image content (bytes) or None on failure.
    """
    try:
        # Encode prompt to be URL safe
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error generating image: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def _get_file_from_result(result):
    """Helper to extract file path from Gradio result."""
    if isinstance(result, str) and os.path.exists(result):
        return result
    if isinstance(result, (list, tuple)):
        # Look for a file path in the result
        for item in result:
            if isinstance(item, str) and os.path.exists(item):
                return item
    return None

def generate_music(prompt, duration=10):
    """
    Generates music using Facebook's MusicGen via HuggingFace Spaces.
    Returns the path to the generated audio file or None.
    """
    try:
        client = Client("facebook/musicgen-small")
        result = client.predict(
            prompt,	# str  in 'Input Text' Textbox component
            None,	# str (filepath or URL to file) in 'File' Audio component
            duration,	# float (numeric value between 1 and 30) in 'Duration' Slider component
            api_name="/predict"
        )
        return _get_file_from_result(result)

    except Exception as e:
        print(f"Error generating music: {e}")
        return None

def generate_video(prompt):
    """
    Generates video using ModelScope via HuggingFace Spaces.
    Returns the path to the generated video file or None.
    """
    try:
        client = Client("damo-vilab/modelscope-damo-text-to-video-synthesis")
        result = client.predict(
            prompt,	# str  in 'Prompt' Textbox component
            -1,	# float  in 'Seed' Number component
            16,	# float (numeric value between 16 and 32) in 'Number of frames' Slider component
            25,	# float (numeric value between 16 and 64) in 'Number of inference steps' Slider component
            api_name="/predict"
        )
        return _get_file_from_result(result)
    except Exception as e:
        print(f"Error generating video: {e}")
        return None
