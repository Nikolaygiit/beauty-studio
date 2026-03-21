# Gemini Ultimate Bot
Это лучший бот на базе моделей Gemini c генерацией изображений, фото, музыки, текста, видео с нуля под ключ.

Проект написан на Python с использованием Streamlit для интерфейса.

## Установка и запуск

1. Установите зависимости:
```bash
pip install -r gemini_bot/requirements.txt
```

2. Запустите приложение из корневой директории:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/gemini_bot && streamlit run gemini_bot/app.py
```

3. Введите свой Google Gemini API Key в боковой панели интерфейса.

## Функционал
- **Текст**: Общение с Gemini-2.0-flash
- **Изображения**: Напишите запрос, начиная со слов `нарисуй`, `фото` или `изображение`. (Использует Pollinations.ai)
- **Музыка**: Напишите запрос, начиная со слов `музыка`, `песня` или `трек`. (Использует sanchit-gandhi/musicgen-streaming через Gradio)
- **Видео**: Напишите запрос, начиная со слов `видео` или `ролик`. (Использует damo-vilab/modelscope-text-to-video-synthesis через Gradio, может быть недоступно из-за RUNTIME_ERROR в Space)
