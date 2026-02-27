import google.generativeai as genai
import streamlit as st
import os

def configure_genai(api_key):
    """Configures the Gemini API with the provided key."""
    if not api_key:
        return False
    genai.configure(api_key=api_key)
    return True

def get_chat_model():
    """Returns the Gemini model instance."""
    return genai.GenerativeModel('gemini-1.5-flash')

def handle_chat_session():
    """Manages the chat session and history."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                model = get_chat_model()
                # Prepare history for the model
                history = [
                    {"role": m["role"], "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]

                chat = model.start_chat(history=history)
                response = chat.send_message(prompt, stream=True)

                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "model", "content": full_response})

            except Exception as e:
                st.error(f"An error occurred: {e}")
