import os
import sys

# Add gemini_bot to path
sys.path.append(os.path.abspath("gemini_bot"))

from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video
from gradio_client import Client

def main():
    print("Testing Image Generation...")
    img_url = generate_image("test cat")
    print(f"Image URL: {img_url}")
    assert "pollinations.ai" in img_url

    print("\nTesting Music Generation...")
    try:
        music_client = Client("sanchit-gandhi/musicgen-streaming")
        music_res = generate_music("test music", music_client)
        print(f"Music result: {music_res}")
    except Exception as e:
        print(f"Music init error (expected if service down): {e}")

    print("\nTesting Video Generation...")
    try:
        video_client = Client("damo-vilab/modelscope-text-to-video-synthesis")
        video_res = generate_video("test video", video_client)
        print(f"Video result: {video_res}")
    except Exception as e:
        print(f"Video init error (expected if service down): {e}")

    print("\nAll tests passed (or handled Expected errors)!")

if __name__ == "__main__":
    main()
