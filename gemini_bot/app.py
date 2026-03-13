import streamlit as st
import os
from modules.text import get_text_client, initialize_chat, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- Configuration ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Sidebar ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

    if st.button("Очистить историю чата"):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        st.rerun()

st.title("✨ Gemini Ultimate Bot")
st.markdown("Могу сгенерировать текст, изображения, музыку и видео!")

# Initialize Gemini chat session if API key is provided
if api_key and "chat_session" not in st.session_state:
    client = get_text_client(api_key)
    if client:
        chat_session = initialize_chat(client)
        if chat_session:
            st.session_state.chat_session = chat_session

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.markdown(msg["content"])
        elif msg["type"] == "image":
            st.image(msg["content"])
        elif msg["type"] == "audio":
            st.audio(msg["content"])
        elif msg["type"] == "video":
            st.video(msg["content"])
        elif msg["type"] == "error":
            st.error(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Напишите сообщение... (для медиа используйте: нарисуй / фото / изображение / музыка / видео)"):

    # 1. Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})

    # 2. Process Assistant Response
    with st.chat_message("assistant"):
        lower_prompt = prompt.lower().strip()

        # --- Image Generation Routing ---
        if any(keyword in lower_prompt for keyword in ["нарисуй", "фото", "изображение"]):
            # Extract actual prompt by removing keywords (simple approach)
            image_prompt = prompt
            for kw in ["нарисуй", "фото", "изображение", "сделай", "создай"]:
                 image_prompt = image_prompt.lower().replace(kw, "").strip()

            if not image_prompt:
                image_prompt = "beautiful landscape" # Fallback

            with st.spinner(f"Генерация изображения по запросу: {image_prompt}..."):
                image_url = generate_image(image_prompt)
                st.image(image_url)
                st.session_state.messages.append({"role": "assistant", "type": "image", "content": image_url})

        # --- Music Generation Routing ---
        elif "музык" in lower_prompt or "песн" in lower_prompt:
            music_prompt = prompt
            for kw in ["сгенерируй", "создай", "сделай", "напиши", "музыку", "музыка", "песню", "песня"]:
                music_prompt = music_prompt.lower().replace(kw, "").strip()

            if not music_prompt:
                music_prompt = "80s pop track with synth and instrumentals" # Fallback

            with st.spinner(f"Генерация музыки по запросу: {music_prompt}..."):
                audio_path = generate_music(music_prompt)
                if isinstance(audio_path, str) and (audio_path.startswith("Error") or "Failed" in audio_path):
                     st.error(audio_path)
                     st.session_state.messages.append({"role": "assistant", "type": "error", "content": audio_path})
                else:
                    st.audio(audio_path)
                    st.session_state.messages.append({"role": "assistant", "type": "audio", "content": audio_path})

        # --- Video Generation Routing ---
        elif "видео" in lower_prompt or "ролик" in lower_prompt:
            video_prompt = prompt
            for kw in ["сгенерируй", "создай", "сделай", "сними", "видео", "ролик"]:
                video_prompt = video_prompt.lower().replace(kw, "").strip()

            if not video_prompt:
                 video_prompt = "a dog playing in the park" # Fallback

            with st.spinner(f"Генерация видео по запросу: {video_prompt}..."):
                video_path = generate_video(video_prompt)
                if isinstance(video_path, str) and (video_path.startswith("Error") or "Failed" in video_path):
                     st.error(video_path)
                     st.session_state.messages.append({"role": "assistant", "type": "error", "content": video_path})
                else:
                     st.video(video_path)
                     st.session_state.messages.append({"role": "assistant", "type": "video", "content": video_path})

        # --- Text Generation (Default to Gemini) ---
        else:
            if not api_key:
                st.warning("Пожалуйста, введите GOOGLE_API_KEY в боковом меню для генерации текста.")
                st.session_state.messages.append({"role": "assistant", "type": "error", "content": "Пожалуйста, введите GOOGLE_API_KEY в боковом меню для генерации текста."})
            elif "chat_session" not in st.session_state:
                 st.error("Ошибка инициализации чата Gemini.")
                 st.session_state.messages.append({"role": "assistant", "type": "error", "content": "Ошибка инициализации чата Gemini."})
            else:
                with st.spinner("Думаю..."):
                    message_placeholder = st.empty()
                    full_response = ""
                    for chunk in generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "type": "text", "content": full_response})
