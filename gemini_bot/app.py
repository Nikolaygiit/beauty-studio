import streamlit as st
from modules.text import render_text_module, clear_chat_history
from modules.image import render_image_module
from modules.music import render_music_module
from modules.video import render_video_module

# Set page config
st.set_page_config(
    page_title="Gemini Ultimate Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .reportview-container {
        margin-top: -2em;
    }
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
</style>
""", unsafe_allow_html=True)

def main():
    # Set default values for session state keys if they don't exist
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''

    # Sidebar
    with st.sidebar:
        st.title("🤖 Gemini Ultimate Bot")
        st.markdown("Универсальный ИИ-ассистент")

        st.header("⚙️ Настройки")

        # API Key input
        api_key_input = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Получите ключ на сайте Google AI Studio",
            value=st.session_state.api_key
        )

        # Update session state if input changes
        if api_key_input != st.session_state.api_key:
            st.session_state.api_key = api_key_input

        if not st.session_state.api_key:
            st.warning("⚠️ Введите API ключ Gemini для работы текстового чата.")
            st.markdown("[Получить ключ здесь](https://aistudio.google.com/app/apikey)")

        st.divider()

        # Navigation
        st.header("🧭 Навигация")
        page = st.radio(
            "Выберите режим:",
            ["💬 Текст (Чат)", "🖼️ Изображения", "🎵 Музыка", "🎬 Видео"]
        )

        st.divider()

        if page == "💬 Текст (Чат)":
            if st.button("🗑️ Очистить историю чата", use_container_width=True):
                clear_chat_history()
                st.success("История очищена!")
                st.rerun()

    # Main content area based on selected page
    if page == "💬 Текст (Чат)":
        render_text_module()
    elif page == "🖼️ Изображения":
        render_image_module()
    elif page == "🎵 Музыка":
        render_music_module()
    elif page == "🎬 Видео":
        render_video_module()

if __name__ == "__main__":
    main()
