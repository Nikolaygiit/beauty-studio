import streamlit as st
import google.generativeai as genai
from modules.text import TextGenerator
from modules.image import ImageGenerator
from modules.music import MusicGenerator
from modules.video import VideoGenerator

st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="✨",
    layout="wide"
)

@st.cache_resource
def get_music_generator():
    return MusicGenerator()

@st.cache_resource
def get_video_generator():
    return VideoGenerator()

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

# Sidebar settings
with st.sidebar:
    st.title("⚙️ Настройки")
    st.session_state.api_key = st.text_input("Введи GOOGLE_API_KEY", type="password", value=st.session_state.api_key)

    st.divider()

    if st.button("🗑️ Очистить историю"):
        st.session_state.chat_history = []
        st.success("История очищена!")

    st.markdown("---")
    st.markdown("""
    ### 🚀 Режимы
    - 📝 **Текст:** Умный чат на базе Gemini 1.5 Flash.
    - 🎨 **Изображения:** Генерация картинок по описанию (через Pollinations.ai).
    - 🎵 **Музыка:** Создание треков (через MusicGen).
    - 🎥 **Видео:** Генерация коротких роликов (через ModelScope).
    """)

# Main title
st.title("✨ Gemini Ultimate Bot")
st.markdown("Единый интерфейс для генерации текста, картинок, музыки и видео!")

# Tabs for different generators
tab_text, tab_image, tab_music, tab_video = st.tabs(["📝 Текст", "🎨 Изображения", "🎵 Музыка", "🎥 Видео"])

# --- TAB: ТЕКСТ ---
with tab_text:
    st.header("Чат с Gemini")
    if not st.session_state.api_key:
        st.warning("⚠️ Пожалуйста, введи GOOGLE_API_KEY в боковой панели.")
    else:
        # Display chat history
        for msg in st.session_state.chat_history:
            role = msg["role"]
            content = msg["content"]
            # Map roles to streamlit UI roles
            avatar = "🤖" if role == "model" else "👤"
            with st.chat_message(role, avatar=avatar):
                st.markdown(content)

        user_input = st.chat_input("Напиши сообщение...")

        if user_input:
            # Display user message immediately
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # Record user message in history
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            with st.spinner("Думаю..."):
                try:
                    text_gen = TextGenerator(api_key=st.session_state.api_key)

                    # Prepare history for Gemini (strictly alternating user/model)
                    gemini_history = []
                    last_role = None
                    for msg in st.session_state.chat_history[:-1]: # exclude the latest user input
                        role = msg["role"]
                        if role != last_role:
                            gemini_history.append({"role": role, "parts": [msg["content"]]})
                            last_role = role
                        else:
                            # If roles are identical (should not happen if alternating strictly, but just in case)
                            gemini_history[-1]["parts"][0] += f"\n\n{msg['content']}"

                    # Generate response
                    response_text = text_gen.generate_response(user_input, gemini_history)

                    with st.chat_message("model", avatar="🤖"):
                        st.markdown(response_text)

                    st.session_state.chat_history.append({"role": "model", "content": response_text})

                except Exception as e:
                    st.error(f"❌ Ошибка генерации текста: {e}")

# --- TAB: ИЗОБРАЖЕНИЯ ---
with tab_image:
    st.header("Генерация изображений")
    img_prompt = st.text_area("Опиши картинку, которую хочешь получить:", "A futuristic city with flying cars at sunset, cyberpunk style")
    img_generate = st.button("🎨 Создать картинку")

    if img_generate and img_prompt:
        with st.spinner("Рисую..."):
            try:
                img_gen = ImageGenerator()
                img_url = img_gen.generate(img_prompt)
                st.image(img_url, caption=img_prompt, use_column_width=True)
            except Exception as e:
                st.error(f"❌ Ошибка генерации картинки: {e}")

# --- TAB: МУЗЫКА ---
with tab_music:
    st.header("Генерация музыки")
    st.markdown("*(Используется модель MusicGen)*")

    music_prompt = st.text_area("Опиши музыку (например, стиль, инструменты):", "80s pop track with synth and instrumentals")

    col1, col2 = st.columns(2)
    with col1:
        music_length = st.slider("Длительность (сек)", min_value=10, max_value=30, value=15)

    music_generate = st.button("🎵 Создать трек")

    if music_generate and music_prompt:
        with st.spinner("Пишу музыку (это может занять некоторое время)..."):
            try:
                music_gen = get_music_generator()
                audio_path = music_gen.generate(music_prompt, music_length)

                if audio_path:
                    st.audio(audio_path)
                    st.success("✅ Готово!")
                else:
                    st.error("Не удалось получить аудиофайл.")

            except Exception as e:
                st.error(f"❌ Ошибка генерации музыки: {e}")

# --- TAB: ВИДЕО ---
with tab_video:
    st.header("Генерация видео")
    st.markdown("*(Используется модель ModelScope Text-to-Video)*")

    video_prompt = st.text_area("Опиши видео:", "A panda eating bamboo in a lush forest")
    video_generate = st.button("🎥 Создать видео")

    if video_generate and video_prompt:
        with st.spinner("Создаю видео (процесс небыстрый, пожалуйста, подожди)..."):
            try:
                video_gen = get_video_generator()
                video_path = video_gen.generate(video_prompt)

                if video_path:
                    st.video(video_path)
                    st.success("✅ Готово!")
                else:
                    st.error("Не удалось получить видеофайл.")
            except Exception as e:
                st.error(f"❌ Ошибка генерации видео: {e}\n\nПопробуйте позже или используйте другой промпт. В данный момент видео-пространство на HuggingFace может быть недоступно.")
