import streamlit as st
import modules.routing as routing
import modules.text as text_module
import modules.image as image_module
import modules.music as music_module
import modules.video as video_module

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="✨")

st.title("✨ Gemini Ultimate Bot")

# Sidebar for API key and clear history
with st.sidebar:
    st.header("Настройки")
    api_key = st.text_input("Введите GOOGLE_API_KEY", type="password", key="api_key_input")

    if st.button("Очистить историю чата"):
        if 'chat_history' in st.session_state:
            del st.session_state['chat_history']
        if 'chat_session' in st.session_state:
            del st.session_state['chat_session']
        if 'gemini_client' in st.session_state:
            del st.session_state['gemini_client']
        st.session_state['current_api_key'] = None
        st.rerun()

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'current_api_key' not in st.session_state:
    st.session_state.current_api_key = None

# Handle API key changes
if api_key and api_key != st.session_state.current_api_key:
    try:
        client, session = text_module.create_chat_session(api_key)
        st.session_state.gemini_client = client
        st.session_state.chat_session = session
        st.session_state.current_api_key = api_key
    except Exception as e:
        st.error(f"Ошибка инициализации Gemini API: {e}")

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"])
        elif msg.get("type") == "audio":
            st.audio(msg["content"])
        elif msg.get("type") == "video":
            st.video(msg["content"])
        else:
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Введите ваш запрос..."):
    if not api_key:
        st.warning("Пожалуйста, введите GOOGLE_API_KEY в настройках.")
        st.stop()

    if 'chat_session' not in st.session_state:
        st.error("Сессия чата не инициализирована. Проверьте API ключ.")
        st.stop()

    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Determine route
    route = routing.route_prompt(prompt)

    with st.chat_message("assistant"):
        if route == "image":
            with st.spinner("Генерация изображения..."):
                url, err = image_module.generate_image_url(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif url:
                    st.image(url)
                    st.session_state.chat_history.append({"role": "assistant", "content": url, "type": "image"})

        elif route == "music":
            with st.spinner("Генерация музыки..."):
                file_path, err = music_module.generate_music(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif file_path:
                    st.audio(file_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": file_path, "type": "audio"})

        elif route == "video":
            with st.spinner("Генерация видео..."):
                file_path, err = video_module.generate_video(prompt)
                if err:
                    st.error(err)
                    st.session_state.chat_history.append({"role": "assistant", "content": err, "type": "text"})
                elif file_path:
                    st.video(file_path)
                    st.session_state.chat_history.append({"role": "assistant", "content": file_path, "type": "video"})

        else: # Text
            with st.spinner("Генерация ответа..."):
                response_container = st.empty()
                full_response = ""
                try:
                    for chunk in text_module.generate_text_stream(st.session_state.chat_session, prompt):
                        if chunk:
                            full_response += chunk
                            response_container.markdown(full_response + "▌")
                    response_container.markdown(full_response)
                    st.session_state.chat_history.append({"role": "assistant", "content": full_response, "type": "text"})
                except Exception as e:
                    st.error(f"Ошибка: {e}")
