from modules.routing import route_prompt

def test_route_prompt_image():
    assert route_prompt("Нарисуй мне кота") == "image"
    assert route_prompt("Покажи фото природы") == "image"

def test_route_prompt_music():
    assert route_prompt("Создай веселую музыку") == "music"
    assert route_prompt("Сгенерируй песню про лето") == "music"

def test_route_prompt_video():
    assert route_prompt("Сделай видео с собакой") == "video"
    assert route_prompt("Короткий клип про город") == "video"

def test_route_prompt_text():
    assert route_prompt("Привет, как дела?") == "text"
    assert route_prompt("Расскажи сказку") == "text"
