from django.test import TestCase
from django.contrib.auth import get_user_model
import tempfile
from ..models import (Tag, Ingredient, Recipe, RecipeIngredient)

User = get_user_model()


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.user = User.objects.create_user(username='test')

        cls.tag = Tag.objects.create(
            name='Тестовый тег 1',
            color='#FFFFFF',
            slug='test_tag_1'
        )
        cls.ingredient = Ingredient.objects.create(
            name='Лук',
            measurement_unit='шт.'
        )
        cls.recipe = Recipe.objects.create(
            name='Луковый пирог',
            text='Вкуснейший пирог на всем свете',
            author=RecipeModelTest.user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            cooking_time=10
        )
        cls.recipe.tags.add(RecipeModelTest.tag)
        cls.recipe.ingredients.add(RecipeModelTest.ingredient,
                                   through_defaults={'amount': 10})


    def test_