import streamlit as st
import os

from modules.text import generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# Application Configuration
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Универсальный бот: текст, генерация изображений, музыки и видео!")

# Sidebar for configuration and history clearing
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google Gemini API Key", type="password", help="Получите ключ в Google AI Studio")
    st.markdown("---")

    if st.button("Очистить историю чата"):
        # Reset session state for chat and Gemini client
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state["chat_session"]
        if "gemini_client" in st.session_state:
            del st.session_state["gemini_client"]
        st.rerun()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
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

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    # Require API key for any generation
    if not api_key:
        st.error("Пожалуйста, введите Google Gemini API Key в боковой панели.")
        st.stop()

    # Display user prompt in chat
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    # Process the prompt based on keywords in Russian
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Генерирую изображение..."):
                image_url = generate_image(prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Генерирую музыку..."):
                result = generate_music(prompt)
                if isinstance(result, tuple) and len(result) > 0:
                    audio_path = result[0]  # Usually the first element is the audio path
                    if audio_path and os.path.exists(audio_path):
                        st.audio(audio_path)
                        st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})
                    else:
                        st.error("Не удалось найти сгенерированный аудио файл.")
                elif isinstance(result, str) and result.startswith("Error"):
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                elif isinstance(result, str) and os.path.exists(result): # Handle case where return is just string path
                    st.audio(result)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": result})
                else:
                    st.error("Неожиданный ответ от сервиса музыки.")

        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Генерирую видео..."):
                result = generate_video(prompt)
                if isinstance(result, str) and "Error" in result:
                     st.error(result)
                     st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                elif isinstance(result, str) and "RUNTIME_ERROR" in result:
                     st.error(result)
                     st.session_state.messages.append({"role": "assistant", "type": "error", "content": result})
                elif result and "video" in result:
                    video_path = result["video"] if isinstance(result, dict) else result[0] # Try to handle different gradio returns
                    if isinstance(video_path, str) and os.path.exists(video_path):
                        st.video(video_path)
                        st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})
                    else:
                         st.error(f"Не удалось воспроизвести видео. Ответ: {result}")
                else:
                    st.video(result) # fallback
                    st.session_state.messages.append({"role": "assistant", "type": "video", "content": result})

        else:
            # Default to Text generation
            response_container = st.empty()
            full_response = ""
            for chunk in generate_text_stream(prompt, api_key):
                full_response += chunk
                response_container.markdown(full_response + "▌")
            response_container.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
