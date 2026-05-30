from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("сделай ФОТО природы") == "image"
    assert get_route("красивое Изображение") == "image"
    assert get_route("картинка с собакой") == "image"

def test_get_route_music():
    assert get_route("включи музыку") == "music"
    assert get_route("напиши ПЕСНЮ про любовь") == "music"
    assert get_route("сделай классный трек") == "music"
    assert get_route("аудио запись") == "music"

def test_get_route_video():
    assert get_route("создай видео про космос") == "video"
    assert get_route("смешной ролик") == "video"
    assert get_route("сделай анимацию") == "video"

def test_get_route_text():
    assert get_route("как дела?") == "text"
    assert get_route("напиши код на python") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("привет") == "text"

def test_get_route_mixed():
    # Проверяем приоритет (видео -> фото -> музыка -> текст)
    assert get_route("нарисуй видео") == "video"
    assert get_route("включи музыку и нарисуй") == "image" # image priority > music
