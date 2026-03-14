from gradio_client import Client

try:
    client_music = Client("sanchit-gandhi/musicgen-streaming")
    print("Music endpoints:")
    print(client_music.view_api(return_format="dict"))
except Exception as e:
    print(f"Music error: {e}")

try:
    client_video = Client("damo-vilab/modelscope-text-to-video-synthesis")
    print("Video endpoints:")
    print(client_video.view_api(return_format="dict"))
except Exception as e:
    print(f"Video error: {e}")
