import streamlit as st
from modules.text import get_client, init_chat_session, stream_text_response
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Session State Initialization ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = ""

# --- Sidebar ---
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("Enter GOOGLE_API_KEY", type="password")

if st.sidebar.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.session_state.chat_session = None
    st.session_state.gemini_client = None
    # Will be re-initialized on next run if API key is present

# Re-initialize client if API key changes
if api_key and api_key != st.session_state.current_api_key:
    st.session_state.current_api_key = api_key
    try:
        client = get_client(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = init_chat_session(client)
    except Exception as e:
        st.sidebar.error(f"Error initializing client: {e}")
        st.session_state.chat_session = None
        st.session_state.gemini_client = None

# --- Main App Logic ---
st.title("Gemini Ultimate Bot 🤖")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])

# --- Chat Input & Routing ---
prompt = st.chat_input("Ask something...")

if prompt:
    # 1. Store and display user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert prompt to lowercase for routing
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        # Image Routing
        if "нарисуй" in prompt_lower or "фото" in prompt_lower or "изображение" in prompt_lower:
            with st.spinner("Generating image..."):
                url, error = generate_image(prompt)
                if url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": url})
                else:
                    st.error(error)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        # Music Routing
        elif "музыка" in prompt_lower or "песня" in prompt_lower or "трек" in prompt_lower:
             with st.spinner("Generating music..."):
                 audio_path, error = generate_music(prompt)
                 if audio_path:
                     st.audio(audio_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_path})
                 else:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        # Video Routing
        elif "видео" in prompt_lower or "ролик" in prompt_lower:
             with st.spinner("Generating video..."):
                 video_path, error = generate_video(prompt)
                 if video_path:
                     st.video(video_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})
                 else:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": error})

        # Text Routing (Default)
        else:
            if not st.session_state.chat_session:
                msg = "Please configure your API key in the sidebar first."
                st.warning(msg)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": msg})
            else:
                response_placeholder = st.empty()
                full_response = ""

                # Use the streamer from the text module
                stream = stream_text_response(st.session_state.chat_session, prompt)

                if stream:
                    for chunk in stream:
                        if chunk.text: # Prevent NoneType concatenation
                            full_response += chunk.text
                            response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
                else:
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": "Failed to get response from Gemini."})
