import streamlit as st
import os

# Import modules
from modules.text import initialize_chat, generate_text
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

# --- App Configuration ---
st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨", layout="wide")
st.title("✨ Gemini Ultimate Bot")
st.markdown("Ваш универсальный ИИ-ассистент: текст, изображения, музыка и видео!")

# --- Sidebar & Initialization ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Gemini API Key:", type="password", help="Получите ключ в Google AI Studio")

    if st.button("Очистить историю чата"):
        st.session_state.chat_history = []
        if 'chat_session' in st.session_state:
            del st.session_state.chat_session
        if 'gemini_client' in st.session_state:
             del st.session_state.gemini_client
        st.session_state.current_api_key = ""
        st.rerun()

    st.markdown("---")
    st.markdown("### Инструкции:")
    st.markdown("- **Текст**: Просто задайте вопрос.\n- **Изображение**: Начните запрос с 'нарисуй', 'фото' или 'изображение'.\n- **Музыка**: Начните запрос с 'музыка', 'песня' или 'трек'.\n- **Видео**: Начните запрос с 'видео' или 'ролик'.")

# --- Session State Management ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = ""

# Re-initialize client if API key changes
if api_key and api_key != st.session_state.current_api_key:
    chat_session, client = initialize_chat(api_key)
    if chat_session:
        st.session_state.chat_session = chat_session
        st.session_state.gemini_client = client
        st.session_state.current_api_key = api_key
        st.success("API ключ успешно применен!")
    else:
        st.error(client) # if chat_session is None, the second return value is the error message
        st.stop()

if not api_key:
    st.warning("Пожалуйста, введите Gemini API Key в боковой панели слева для начала работы.")
    st.stop()

if 'chat_session' not in st.session_state:
    st.error("Сессия чата не инициализирована. Проверьте API ключ.")
    st.stop()

# --- Display Chat History ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
             st.image(message["content"])
             st.markdown(f"*(Сгенерировано по запросу: {message['prompt']})*")
        elif message["type"] == "music":
             st.audio(message["content"])
             st.markdown(f"*(Музыка по запросу: {message['prompt']})*")
        elif message["type"] == "video":
             st.video(message["content"])
             st.markdown(f"*(Видео по запросу: {message['prompt']})*")
        elif message["type"] == "error":
             st.error(message["content"])


# --- Chat Input & Routing ---
prompt = st.chat_input("Введите ваш запрос...")

if prompt:
    # Display user prompt
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})

    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):

            # --- Image Generation Routing ---
            if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
                 st.markdown("🎨 Генерирую изображение...")
                 media_url, error = generate_image(prompt)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                 else:
                     st.image(media_url)
                     st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": media_url, "prompt": prompt})

            # --- Music Generation Routing ---
            elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
                 st.markdown("🎵 Генерирую музыку (это может занять некоторое время)...")
                 media_path, error = generate_music(prompt)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                 else:
                     st.audio(media_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": media_path, "prompt": prompt})

            # --- Video Generation Routing ---
            elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
                 st.markdown("🎥 Генерирую видео (это может занять несколько минут)...")
                 media_path, error = generate_video(prompt)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                 else:
                     st.video(media_path)
                     st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": media_path, "prompt": prompt})

            # --- Text Generation Routing (Default) ---
            else:
                 text_response, error = generate_text(prompt, st.session_state.chat_session)
                 if error:
                     st.error(error)
                     st.session_state.chat_history.append({"role": "assistant", "type": "error", "content": error})
                 else:
                     st.markdown(text_response)
                     st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": text_response})
