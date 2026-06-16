from modules.routing import get_route

def test_get_route_image():
    assert get_route("Нарисуй мне кота") == "image"
    assert get_route("Сделай фото леса") == "image"

def test_get_route_music():
    assert get_route("Включи музыку") == "music"
    assert get_route("Напиши песню о любви") == "music"

def test_get_route_video():
    assert get_route("Сделай видео с морем") == "video"
    assert get_route("Сними ролик про собак") == "video"

def test_get_route_text():
    assert get_route("Как дела?") == "text"
    assert get_route("Напиши код на python") == "text"
