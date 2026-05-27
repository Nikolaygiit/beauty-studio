import streamlit as st
from modules.text import init_gemini_client, generate_text_stream
from modules.image import generate_image
from modules.music import generate_music
from modules.video import generate_video

st.set_page_config(page_title="Gemini Ultimate Bot", layout="wide")

st.title("Gemini Ultimate Bot 🚀")
st.markdown("Универсальный бот: текст, изображения, музыка и видео!")

# Sidebar config
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите ваш Google API Key", type="password")

    if st.button("Очистить историю чата"):
        for key in ["chat_history", "chat_session", "gemini_client", "current_api_key"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("История очищена!")
        st.rerun()

if not api_key:
    st.info("Пожалуйста, введите ваш Google API Key в боковой панели, чтобы начать.")
    st.stop()

# Initialize Gemini Client and ensure session state is set
try:
    init_gemini_client(api_key)
except Exception as e:
    st.error(f"Ошибка инициализации Gemini API: {e}")
    st.stop()

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Введите ваш запрос... (например: 'нарисуй кота', 'песня о лете', 'видео заката')"):

    # Store and display user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    prompt_lower = prompt.lower()

    # Simple routing based on Russian keywords
    with st.chat_message("assistant"):
        if any(kw in prompt_lower for kw in ['нарисуй', 'фото', 'изображение']):
            st.markdown("Генерирую изображение...")
            url, err = generate_image(prompt)
            if err:
                st.error(err)
                st.session_state.chat_history.append({"role": "assistant", "content": err})
            else:
                st.image(url, caption=prompt)
                st.session_state.chat_history.append({"role": "assistant", "content": f"![Сгенерированное изображение]({url})"})

        elif any(kw in prompt_lower for kw in ['музык', 'песн', 'песен', 'трек']):
            st.markdown("Генерирую музыку... (это может занять некоторое время)")
            with st.spinner("Создание трека..."):
                audio_path, err = generate_music(prompt)
            if err:
                st.error(err)
                st.session_state.chat_history.append({"role": "assistant", "content": err})
            else:
                st.audio(audio_path)
                st.session_state.chat_history.append({"role": "assistant", "content": f"Музыка сгенерирована по запросу: {prompt}"})

        elif any(kw in prompt_lower for kw in ['видео', 'ролик']):
            st.markdown("Генерирую видео... (это может занять до нескольких минут)")
            with st.spinner("Создание видео..."):
                video_path, err = generate_video(prompt)
            if err:
                st.error(err)
                st.session_state.chat_history.append({"role": "assistant", "content": err})
            else:
                st.video(video_path)
                st.session_state.chat_history.append({"role": "assistant", "content": f"Видео сгенерировано по запросу: {prompt}"})

        else:
            # Default text generation
            response_placeholder = st.empty()
            full_response = ""
            for chunk in generate_text_stream(prompt):
                full_response += chunk
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
