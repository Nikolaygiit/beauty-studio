import streamlit as st
import google.generativeai as genai
from gradio_client import Client
import traceback

# Import modules
from modules.text import generate_text_response
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

# --- CACHING GRADIO CLIENTS ---
@st.cache_resource(show_spinner=False)
def get_music_client():
    try:
        return Client("sanchit-gandhi/musicgen-streaming")
    except Exception as e:
        st.sidebar.error(f"Error loading Music Gen Client: {e}")
        return None

@st.cache_resource(show_spinner=False)
def get_video_client():
    try:
        return Client("damo-vilab/modelscope-text-to-video-synthesis")
    except Exception as e:
        st.sidebar.error(f"Error loading Video Gen Client: {e}")
        return None

# Load clients in background
MUSIC_CLIENT = get_music_client()
VIDEO_CLIENT = get_video_client()


# --- SIDEBAR & SETUP ---
st.sidebar.title("⚙️ Settings")

# API Key Input
google_api_key = st.sidebar.text_input("Enter GOOGLE_API_KEY", type="password")
if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    st.sidebar.warning("Please enter your Google API Key to use text generation.")

# Mode Selector
st.sidebar.markdown("---")
mode = st.sidebar.radio(
    "Select Mode",
    ["Text Chat", "Image Generation", "Music Generation", "Video Generation"]
)

# Clear Chat History Button
if st.sidebar.button("Clear Chat History"):
    st.session_state.gemini_chat_session = None
    st.session_state.messages = []
    st.rerun()

# --- MAIN APP UI ---
st.title(f"Gemini Ultimate Bot - {mode}")

# Initialize chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Render media if present
        if "image" in message:
            st.image(message["image"])
        if "audio" in message:
            st.audio(message["audio"])
        if "video" in message:
            st.video(message["video"])

# User Input
if prompt := st.chat_input("Enter your prompt..."):
    # Store user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # TEXT CHAT
        if mode == "Text Chat":
            if not google_api_key:
                st.error("Please configure GOOGLE_API_KEY in the sidebar.")
            else:
                try:
                    for chunk in generate_text_response(prompt):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        # IMAGE GENERATION
        elif mode == "Image Generation":
            try:
                message_placeholder.markdown(f"Generating image for: *{prompt}*...")
                image_url = generate_image_url(prompt)
                st.image(image_url)
                message_placeholder.empty()
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Generated image for: *{prompt}*",
                    "image": image_url
                })
            except Exception as e:
                st.error(f"Failed to generate image: {e}")

        # MUSIC GENERATION
        elif mode == "Music Generation":
            if not MUSIC_CLIENT:
                st.error("Music Generation service is currently unavailable.")
            else:
                try:
                    message_placeholder.markdown(f"Generating music for: *{prompt}*... (This may take a minute)")
                    audio_path = generate_music(MUSIC_CLIENT, prompt)
                    st.audio(audio_path)
                    message_placeholder.empty()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Generated music for: *{prompt}*",
                        "audio": audio_path
                    })
                except Exception as e:
                    st.error(f"Failed to generate music: {e}")
                    print(traceback.format_exc())

        # VIDEO GENERATION
        elif mode == "Video Generation":
            if not VIDEO_CLIENT:
                st.error("Video Generation service is currently unavailable.")
            else:
                try:
                    message_placeholder.markdown(f"Generating video for: *{prompt}*... (This may take a while)")
                    # The client predict currently returns a string path directly or tuple depending on version,
                    # check actual return structure.
                    video_res = generate_video(VIDEO_CLIENT, prompt)
                    # Handle return format which is typically dict with 'video' key or direct string
                    if isinstance(video_res, dict) and 'video' in video_res:
                        video_path = video_res['video']
                    else:
                        video_path = video_res

                    st.video(video_path)
                    message_placeholder.empty()
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Generated video for: *{prompt}*",
                        "video": video_path
                    })
                except Exception as e:
                    st.error(f"Failed to generate video: {e}")
                    print(traceback.format_exc())
