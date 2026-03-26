import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("Gemini Ultimate Bot 🤖")

# Sidebar for configuration
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google Gemini API Key:", type="password")

    if st.button("Очистить историю чата"):
        if 'chat_session' in st.session_state:
            del st.session_state['chat_session']
        if 'messages' in st.session_state:
            st.session_state.messages = []
        st.success("История чата очищена!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            st.audio(message["content"])
        elif message["type"] == "video":
            st.video(message["content"])
        elif message["type"] == "error":
            st.error(message["content"])

# Accept user input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    # Routing logic based on keywords
    prompt_lower = prompt.lower()
    is_image = any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"])
    is_music = any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"])
    is_video = any(keyword in prompt_lower for keyword in ["видео", "ролик"])

    with st.chat_message("assistant"):
        if is_image:
            with st.spinner("Генерация изображения..."):
                image_url = image.generate_image_url(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})
        elif is_music:
            with st.spinner("Генерация музыки..."):
                result = music.generate_music(prompt)
                if isinstance(result, str) and (result.startswith("Ошибка") or result.startswith("Произошла ошибка")):
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                else:
                    # Assuming result is a tuple like (audio_path, None) or similar from Gradio
                    # The exact return structure depends on the Gradio space
                    # Usually it's a file path to the generated audio
                    if isinstance(result, tuple) and len(result) > 0:
                        audio_path = result[0]
                    else:
                        audio_path = result
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})
        elif is_video:
            with st.spinner("Генерация видео..."):
                result = video.generate_video(prompt)
                if isinstance(result, str) and (result.startswith("Ошибка") or result.startswith("Произошла ошибка")):
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                else:
                    # The return is usually a path to the generated video file
                    st.video(result)
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": result})
        else:
            if not api_key:
                st.warning("Пожалуйста, введите ваш Google Gemini API Key в боковой панели для генерации текста.")
                st.stop()
            else:
                with st.spinner("Генерация ответа..."):
                    # Use st.write_stream to handle the generator
                    response_stream = text.generate_text_response(api_key, prompt)
                    # We need to collect the chunks to save to history, but write_stream can consume it
                    # Let's use a placeholder and manually append
                    placeholder = st.empty()
                    full_response = ""
                    for chunk in response_stream:
                        if chunk.startswith("Произошла ошибка"):
                            st.error(chunk)
                            full_response = chunk
                            break
                        full_response += chunk
                        placeholder.markdown(full_response + "▌")
                    if not full_response.startswith("Произошла ошибка"):
                        placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
                    else:
                        st.session_state.messages.append({"role": "assistant", "type": "error", "content": full_response})
