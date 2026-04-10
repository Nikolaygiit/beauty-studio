import streamlit as st
import sys
import os

# Add the parent directory to sys.path so modules can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.text import init_chat_session, generate_text_response
from modules.image import generate_image_url
from modules.music import generate_music
from modules.video import generate_video

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

st.title("Gemini Ultimate Bot 🤖")
st.markdown("Генерация текста, изображений, музыки и видео с помощью Gemini и других моделей.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите Google API Key:", type="password")

    if st.button("Очистить историю чата"):
        # Reset session state
        keys_to_clear = ['chat_history', 'chat_session', 'gemini_client', 'current_api_key']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История чата очищена.")

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = None

# Re-initialize chat session if API key changes
if api_key and api_key != st.session_state.current_api_key:
    if init_chat_session(api_key):
        st.session_state.current_api_key = api_key
        st.success("Сессия Gemini успешно инициализирована!")

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"])
        elif message["type"] == "audio":
            if message["content"].endswith(".wav") or message["content"].endswith(".mp3"):
                st.audio(message["content"])
            else:
                st.markdown(message["content"]) # Error message
        elif message["type"] == "video":
            if message["content"].endswith(".mp4") or message["content"].endswith(".webm"):
                st.video(message["content"])
            else:
                st.markdown(message["content"]) # Error message

# --- HANDLE USER INPUT ---
prompt = st.chat_input("Напишите ваш запрос здесь...")

if prompt:
    # Check if API key is provided for text chat
    if not api_key:
        st.warning("Пожалуйста, введите ваш Google API Key в боковой панели для текстовых запросов к Gemini.")

    # Display user message
    st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert prompt to lowercase for keyword matching
    prompt_lower = prompt.lower()

    # Routing logic
    with st.chat_message("assistant"):
        if any(keyword in prompt_lower for keyword in ['нарисуй', 'фото', 'изображение']):
            with st.spinner("Генерация изображения..."):
                image_url = generate_image_url(prompt)
                st.image(image_url)
                st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": image_url})

        elif any(keyword in prompt_lower for keyword in ['музыка', 'песня', 'трек']):
            with st.spinner("Генерация музыки... Это может занять некоторое время."):
                audio_result = generate_music(prompt)

                # Check if audio_result is a string (error message) or a file path tuple/list from gradio
                # Usually gradio returns a tuple where the first element is the path, or just the path string if it's a file path
                if isinstance(audio_result, str) and not audio_result.startswith("Ошибка") and not audio_result.startswith("Произошла ошибка") and (audio_result.endswith(".wav") or audio_result.endswith(".mp3") or os.path.exists(audio_result)):
                    st.audio(audio_result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_result})
                elif isinstance(audio_result, tuple) and len(audio_result) > 0 and isinstance(audio_result[0], str):
                     st.audio(audio_result[0])
                     st.session_state.chat_history.append({"role": "assistant", "type": "audio", "content": audio_result[0]})
                else:
                    st.markdown(str(audio_result))
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": str(audio_result)})

        elif any(keyword in prompt_lower for keyword in ['видео', 'ролик']):
            with st.spinner("Генерация видео... Это может занять несколько минут."):
                video_result = generate_video(prompt)

                if isinstance(video_result, str) and not video_result.startswith("Ошибка") and not video_result.startswith("Произошла ошибка") and (video_result.endswith(".mp4") or os.path.exists(video_result)):
                    st.video(video_result)
                    st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_result})
                elif isinstance(video_result, dict) and "video" in video_result:
                     st.video(video_result["video"])
                     st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_result["video"]})
                else:
                    st.markdown(str(video_result))
                    st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": str(video_result)})

        else:
            # Default to text generation via Gemini
            if api_key and 'chat_session' in st.session_state:
                with st.spinner("Gemini печатает..."):
                    response_stream = generate_text_response(prompt)
                    if response_stream:
                        # Streamlit streaming container
                        full_response = st.write_stream(response_stream)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})
            else:
                 st.error("Невозможно сгенерировать ответ. Сессия чата не инициализирована. Проверьте API ключ.")
