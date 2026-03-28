import streamlit as st
from modules import text, image, music, video

st.set_page_config(page_title="Gemini Ultimate Bot", page_icon="🤖")

st.title("🤖 Gemini Ultimate Bot")
st.markdown("Бот на базе моделей Gemini с генерацией текста, изображений, музыки и видео.")

# Sidebar setup
st.sidebar.title("Настройки")
api_key = st.sidebar.text_input("Введите ваш Google API Key", type="password")

if st.sidebar.button("Очистить историю чата"):
    st.session_state.messages = []
    text.reset_chat_session()
    st.sidebar.success("История чата очищена!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display associated media if present
        if "image_url" in message:
            st.image(message["image_url"])
        if "audio_path" in message:
            st.audio(message["audio_path"])
        if "video_path" in message:
            st.video(message["video_path"])

# Accept user input
if prompt := st.chat_input("Напишите сообщение (напр. 'нарисуй кота', 'музыка пианино', 'видео закат')..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Analyze prompt for routing
    prompt_lower = prompt.lower()

    with st.chat_message("assistant"):
        message_data = {"role": "assistant"}

        # Check for image generation
        if any(keyword in prompt_lower for keyword in ["нарисуй", "фото", "изображение"]):
            with st.spinner("Создаю изображение..."):
                st.markdown(f"**Запрос на изображение:** {prompt}")
                image_url = image.get_image_url(prompt)

                if image_url.startswith("Ошибка"):
                    st.error(image_url)
                    message_data["content"] = image_url
                else:
                    st.image(image_url)
                    message_data["content"] = f"Вот ваше изображение по запросу: {prompt}"
                    message_data["image_url"] = image_url

        # Check for music generation
        elif any(keyword in prompt_lower for keyword in ["музыка", "песня", "трек"]):
            with st.spinner("Создаю музыку... Это может занять несколько минут."):
                st.markdown(f"**Запрос на музыку:** {prompt}")
                audio_result = music.generate_music(prompt)

                if isinstance(audio_result, str) and audio_result.startswith("Ошибка"):
                    st.error(audio_result)
                    message_data["content"] = audio_result
                else:
                    # audio_result might be a tuple (audio_path, ...) depending on Gradio output
                    audio_path = audio_result[0] if isinstance(audio_result, (list, tuple)) else audio_result
                    st.audio(audio_path)
                    message_data["content"] = f"Вот ваша музыка по запросу: {prompt}"
                    message_data["audio_path"] = audio_path

        # Check for video generation
        elif any(keyword in prompt_lower for keyword in ["видео", "ролик"]):
            with st.spinner("Создаю видео... Это может занять несколько минут."):
                st.markdown(f"**Запрос на видео:** {prompt}")
                video_result = video.generate_video(prompt)

                if isinstance(video_result, str) and video_result.startswith("Ошибка"):
                    st.error(video_result)
                    message_data["content"] = video_result
                elif isinstance(video_result, dict) and "video" in video_result:
                     video_path = video_result["video"]
                     st.video(video_path)
                     message_data["content"] = f"Вот ваше видео по запросу: {prompt}"
                     message_data["video_path"] = video_path
                else:
                    # video_result might be a tuple or string path depending on Gradio output
                    video_path = video_result[0] if isinstance(video_result, (list, tuple)) else video_result
                    st.video(video_path)
                    message_data["content"] = f"Вот ваше видео по запросу: {prompt}"
                    message_data["video_path"] = video_path

        # Default to text generation (Gemini)
        else:
            if not api_key:
                response = "Пожалуйста, введите ваш Google API Key в боковой панели, чтобы общаться со мной."
                st.markdown(response)
                message_data["content"] = response
            else:
                with st.spinner("Думаю..."):
                    # Use the text module to get streaming response
                    response_stream = text.get_text_response(prompt, api_key)

                    if isinstance(response_stream, str) and response_stream.startswith("Произошла ошибка"):
                        st.error(response_stream)
                        message_data["content"] = response_stream
                    else:
                        # Stream the response
                        def stream_generator():
                            for chunk in response_stream:
                                yield chunk.text

                        response_text = st.write_stream(stream_generator())
                        message_data["content"] = response_text

        # Save assistant message to chat history
        st.session_state.messages.append(message_data)
