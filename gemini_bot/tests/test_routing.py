from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("нарисуй кота") == "image"
    assert route_prompt("сгенерируй фото собаки") == "image"
    assert route_prompt("покажи изображение леса") == "image"
    assert route_prompt("сгенерируй изображение") == "image"

def test_route_prompt_music():
    assert route_prompt("сгенерируй музыку для отдыха") == "music"
    assert route_prompt("напиши песню о любви") == "music"
    assert route_prompt("сделай трек в стиле рок") == "music"

def test_route_prompt_video():
    assert route_prompt("создай видео с морем") == "video"
    assert route_prompt("сними ролик про котов") == "video"
    assert route_prompt("сгенерируй видео леса") == "video"

def test_route_prompt_text():
    assert route_prompt("привет, как дела?") == "text"
    assert route_prompt("расскажи о теории относительности") == "text"
    # Ensure substring match inside unrelated word doesn't route incorrectly
    assert route_prompt("расскажи про фотосинтез") == "text"
