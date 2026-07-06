from modules.routing import get_route

def test_routing_image():
    assert get_route("Нарисуй мне красивый пейзаж") == "image"
    assert get_route("Покажи фото кота") == "image"
    assert get_route("Сделай фотографию") == "image"
    assert get_route("Создай изображение") == "image"
    # Negative test
    assert get_route("фотосинтез") == "text"

def test_routing_music():
    assert get_route("Включи музыку") == "music"
    assert get_route("Спой песню") == "music"
    assert get_route("Напиши веселую песенку") == "music"
    assert get_route("Крутой трек") == "music"

def test_routing_video():
    assert get_route("Сделай видео про космос") == "video"
    assert get_route("Смешной ролик") == "video"

def test_routing_text():
    assert get_route("Привет, как дела?") == "text"
    assert get_route("Расскажи сказку") == "text"
    assert get_route("Что такое нейросеть?") == "text"
