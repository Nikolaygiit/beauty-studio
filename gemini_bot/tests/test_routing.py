from modules.routing import get_route

def test_get_route_image():
    assert get_route("нарисуй кота") == "image"
    assert get_route("фото собаки") == "image"
    assert get_route("сделай изображение леса") == "image"

def test_get_route_music():
    assert get_route("сочини музыку") == "music"
    assert get_route("включи песню") == "music"
    assert get_route("создай трек") == "music"

def test_get_route_video():
    assert get_route("сделай видео про космос") == "video"
    assert get_route("короткий ролик") == "video"

def test_get_route_text():
    assert get_route("привет, как дела?") == "text"
    assert get_route("расскажи сказку") == "text"
    assert get_route("что такое питон?") == "text"
