import os
from gradio_client import Client
import time

def generate_music(prompt, duration=10, token=None):
    """
    Generates music using Facebook's MusicGen Space.

    Args:
        prompt (str): Description of the music.
        duration (int): Duration in seconds.
        token (str): HF Token (optional).

    Returns:
        str: Path to the generated audio file, or None if failed.
    """
    token = token or os.getenv("HF_TOKEN")
    try:
        print(f"Connecting to MusicGen for prompt: {prompt}")
        client = Client("facebook/MusicGen", hf_token=token)

        # Note: The API parameters for MusicGen might change.
        # Standard: text, file (optional), duration
        result = client.predict(
            prompt,	# str  in 'Describe your music' Textbox component
            None,	# str (filepath or URL to file) in 'File' Audio component
            api_name="/predict"
        )

        # Result is usually a tuple/list. The audio file path is often the first or second element.
        # Let's inspect what we get. Usually it returns the path to the temporary file.
        # MusicGen returns (sampling_rate, audio_array) in some contexts, or filepath in others.
        # Gradio Client usually returns filepath.

        return result
    except Exception as e:
        print(f"Error generating music: {e}")
        return None

def generate_video(prompt, token=None):
    """
    Generates video using ModelScope Space.

    Args:
        prompt (str): Description of the video.
        token (str): HF Token.

    Returns:
        str: Path to the generated video file, or None if failed.
    """
    space_name = os.getenv("VIDEO_SPACE_NAME", "damo-vilab/modelscope-text-to-video-synthesis")
    token = token or os.getenv("HF_TOKEN")

    try:
        print(f"Connecting to Video Space ({space_name}) for prompt: {prompt}")
        client = Client(space_name, hf_token=token)

        # ModelScope usually takes just the prompt
        result = client.predict(
            prompt,	# str  in 'Prompt' Textbox component
            -1,	# float  in 'Seed' Number component
            16,	# float  in 'Number of frames' Number component
            25,	# float  in 'Number of inference steps' Number component
            api_name="/infer"
        )

        # Result is typically the path to the video file
        return result[0] if isinstance(result, (list, tuple)) else result

    except Exception as e:
        print(f"Error generating video: {e}")
        # Fallback/Retry logic could go here
        return None
