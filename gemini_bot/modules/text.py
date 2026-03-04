import streamlit as st
import google.generativeai as genai
import traceback

def get_gemini_client():
    if "api_key" in st.session_state and st.session_state.api_key:
        try:
            genai.configure(api_key=st.session_state.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            return model
        except Exception as e:
            st.error(f"Ошибка настройки Gemini API: {e}")
            return None
    return None

def clear_chat_history():
    st.session_state.chat_history = []
    if "chat_session" in st.session_state:
        del st.session_state.chat_session

def render_text_module():
    st.header("💬 Чат с Gemini (Текст и код)")

    if "api_key" not in st.session_state or not st.session_state.api_key:
        st.warning("Пожалуйста, введите API ключ Gemini в боковой панели слева для использования чата.")
        st.info("💡 Изображения, Музыку и Видео можно генерировать без ключа Gemini!")
        return

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    model = get_gemini_client()
    if not model:
        return

    if "chat_session" not in st.session_state:
        try:
            st.session_state.chat_session = model.start_chat(history=[])
        except Exception as e:
            st.error(f"Ошибка инициализации чата: {e}")
            return

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Спросите что-нибудь у Gemini..."):
        # Display user message in chat message container immediately
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                with st.spinner('Gemini думает...'):
                    # Recreate history for strict role alternation required by Gemini API
                    # The Google Generative AI requires strictly alternating "user" and "model" roles
                    formatted_history = []
                    last_role = None

                    for msg in st.session_state.chat_history[:-1]: # exclude the latest prompt
                        role = "model" if msg["role"] == "assistant" else "user"

                        # Fix consecutive same-role messages by merging them
                        if last_role == role:
                            formatted_history[-1]["parts"][0] += f"\n\n{msg['content']}"
                        else:
                            formatted_history.append({"role": role, "parts": [msg["content"]]})

                        last_role = role

                    # If the very last message in formatted history is also "user",
                    # we must append a dummy model message or merge with prompt
                    # But actually start_chat takes history, and send_message takes the next user prompt
                    # So the last message in history MUST be "model" or history empty
                    if formatted_history and formatted_history[-1]["role"] == "user":
                        # We have a hanging user message. Let's merge the current prompt into it
                        # or just drop the old one
                        formatted_history.pop()

                    # Restart chat with properly formatted history to avoid state corruption
                    st.session_state.chat_session = model.start_chat(history=formatted_history)

                    # Send message
                    response = st.session_state.chat_session.send_message(prompt, stream=True)

                    for chunk in response:
                        if chunk.text:
                            full_response += chunk.text
                            message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)

            except Exception as e:
                error_msg = f"Произошла ошибка при обращении к API: {str(e)}"
                st.error(error_msg)

                # If there's an API error, we should probably remove the user's message from history
                # so they can try again without breaking the strict alternation rule
                if st.session_state.chat_history and st.session_state.chat_history[-1]["role"] == "user":
                    st.session_state.chat_history.pop()
                return # Exit early so we don't save the error response

        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
