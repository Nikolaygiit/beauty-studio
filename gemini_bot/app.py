import streamlit as st

# Настройка страницы
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide"
)

from modules import text, image, music, video, routing

def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None
    if "current_api_key" not in st.session_state:
        st.session_state.current_api_key = ""

def clear_chat():
    st.session_state.chat_history = []
    st.session_state.gemini_client = None
    st.session_state.chat_session = None
    # При следующей отправке сообщения сессия пересоздастся

def main():
    init_session_state()

    st.title("🤖 Gemini Ultimate Bot")
    st.markdown("Бот, умеющий генерировать **текст, изображения, музыку и видео** по вашим запросам на русском языке.")

    # Сайдбар с настройками
    with st.sidebar:
        st.header("Настройки")
        api_key = st.text_input("Введите GOOGLE_API_KEY", type="password")

        # Переинициализация сессии при смене ключа
        if api_key and api_key != st.session_state.current_api_key:
            st.session_state.current_api_key = api_key
            st.session_state.gemini_client, st.session_state.chat_session = text.init_chat_session(api_key)
            st.success("API ключ применён!")

        st.button("Очистить историю", on_click=clear_chat)

    # Отображение истории чата
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg["type"] == "text":
                st.markdown(msg["content"])
            elif msg["type"] == "image":
                st.image(msg["content"])
            elif msg["type"] == "music":
                st.audio(msg["content"])
            elif msg["type"] == "video":
                st.video(msg["content"])

    # Ввод пользователя
    prompt = st.chat_input("Напишите ваш запрос...")
    if prompt:
        if not st.session_state.current_api_key:
            st.error("Пожалуйста, введите GOOGLE_API_KEY в боковом меню.")
            return

        # Инициализация сессии, если была очищена
        if st.session_state.chat_session is None:
            st.session_state.gemini_client, st.session_state.chat_session = text.init_chat_session(st.session_state.current_api_key)

        # Добавляем запрос пользователя
        st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Определяем тип запроса
        route = routing.route_prompt(prompt)

        # Обработка в зависимости от маршрута
        with st.chat_message("assistant"):
            if route == "image":
                with st.spinner("Генерация изображения..."):
                    img_url, err = image.generate_image(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                    else:
                        st.image(img_url)
                        st.session_state.chat_history.append({"role": "assistant", "type": "image", "content": img_url})

            elif route == "music":
                with st.spinner("Генерация музыки (это может занять время)..."):
                    audio_path, err = music.generate_music(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                    else:
                        st.audio(audio_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "music", "content": audio_path})

            elif route == "video":
                with st.spinner("Генерация видео (это может занять значительное время)..."):
                    video_path, err = video.generate_video(prompt)
                    if err:
                        st.error(err)
                        st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": err})
                    else:
                        st.video(video_path)
                        st.session_state.chat_history.append({"role": "assistant", "type": "video", "content": video_path})

            else:  # route == "text"
                placeholder = st.empty()
                full_response = ""
                with st.spinner("Gemini печатает..."):
                    for chunk in text.generate_text_stream(st.session_state.chat_session, prompt):
                        full_response += chunk
                        placeholder.markdown(full_response + "▌")
                placeholder.markdown(full_response)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": full_response})

if __name__ == "__main__":
    main()
