import streamlit as st
import modules.text as text_gen
import modules.image as image_gen
import modules.music as music_gen
import modules.video as video_gen

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.title("Gemini Ultimate Bot")

# Sidebar
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        for key in ["chat_history", "chat_session", "gemini_client", "current_api_key"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История чата очищена!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history on app rerun
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            if isinstance(message["content"], tuple) and len(message["content"]) > 1:
                st.audio(message["content"][1])
            else:
                 st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# Accept user input
if prompt := st.chat_input("Напишите ваш запрос..."):
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Route request based on Russian keywords
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            # Image Generation
            with st.spinner("Генерирую изображение..."):
                image_url = image_gen.generate_image(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            # Music Generation
            with st.spinner("Генерирую музыку (это может занять время)..."):
                result = music_gen.generate_music(prompt)
                if isinstance(result, str) and result.startswith("Ошибка"):
                    st.error(result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": result})
                else:
                    # Gradio generate_audio returns a tuple (sample_rate, audio_data) usually, or the file path
                    if isinstance(result, tuple) and len(result) > 1:
                         st.audio(result[1])
                    else:
                         st.audio(result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": result})

        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            # Video Generation
            with st.spinner("Генерирую видео (это может занять значительное время)..."):
                result = video_gen.generate_video(prompt)
                if isinstance(result, str) and result.startswith("Ошибка"):
                    st.error(result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": result})
                else:
                    st.video(result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": result})

        else:
            # Text Generation
            if not api_key:
                st.warning("Пожалуйста, введите Google API Key в боковой панели для генерации текста.")
                st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": "API Key не предоставлен."})
            else:
                with st.spinner("Думаю..."):
                    # Use a placeholder for streaming
                    response_placeholder = st.empty()
                    full_response = ""
                    for chunk in text_gen.generate_text(prompt, api_key):
                        full_response += chunk
                        response_placeholder.markdown(full_response + "▌")
                    response_placeholder.markdown(full_response)

                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
