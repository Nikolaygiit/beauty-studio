import streamlit as st
from gradio_client import Client

@st.cache_resource
def get_music_client():
    return Client("sanchit-gandhi/musicgen-streaming")

def handle_music_generation():
    st.header("Music Generation")
    prompt = st.text_input("Enter a prompt for the music:", "A catchy pop song about coding")

    if st.button("Generate Music"):
        if prompt:
            try:
                with st.spinner("Generating music... (this may take a minute)"):
                    client = get_music_client()
                    result = client.predict(
                        prompt,	# str  in 'Input Text' Textbox component
                        fn_index=0
                    )
                    # result is a tuple. For 'sanchit-gandhi/musicgen-streaming', the second element
                    # (index 1) is typically the path to the generated audio file.

                    if result:
                         audio_path = result[1]
                         st.audio(audio_path)
            except Exception as e:
                st.error(f"Error generating music: {e}")
        else:
            st.warning("Please enter a prompt.")
