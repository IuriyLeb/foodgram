import tempfile

test_user_1 = {
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkins",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "vaavavav9900"
}

test_user_2 = {
    "email": "test2@test.com",
    "username": "test2",
    "first_name": "Test",
    "last_name": "Two",
    "password": "TestTw0_1"
}

test_tag_1 = {
    "name": "Тестовый тег 1",
    "color": "#FFFFFF",
    "slug": "test_tag_1"
}

test_tag_2 = {
    "name": "Тестовый тег 2",
    "color": "#FFFFFF",
    "slug": "test_tag_2"
}

test_ingredient_1 = {
    "name": "Лук",
    "measurement_unit": "шт."
}

test_ingredient_2 = {
    "name": "Морковь",
    "measurement_unit": "кг."
}

test_recipe_1 = {

    "name": "Луковый пирог",
    "text": "Вкуснейший пирог на всем свете",
    "image": tempfile.NamedTemporaryFile(suffix=".jpg").name,
    "cooking_time": 10
}

test_recipe_2 = {
    "name": "Морковный пирог",
    "text": "Лучший морковный",
    "image": tempfile.NamedTemporaryFile(suffix=".jpg").name,
    "cooking_time": 10
}

test_create_recipe_1 = {
    "ingredients": [
        {
            "id": 1,
            "amount": 10
        }
    ],
    "tags": [1, 2],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "Тестовый рецепт",
    "text": "Тестовый рецепт",
    "cooking_time": 5
}

test_create_recipe_2 = {
    "ingredients": [
        {
            "id": 1,
            "amount": 10
        }
    ],
    "tags": [1, 2],
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
    "name": "Тестовый рецепт",
    "text": "Тестовый рецепт",
    "cooking_time": 20
}