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

    def test_models_have_correct_object_names(self):
        """У моделей корректно работает __str__."""
        tag = RecipeModelTest.tag
        ingredient = RecipeModelTest.ingredient
        recipe = RecipeModelTest.recipe

        expected_tag_name = tag.name
        expected_ingredient_name = f'{ingredient.name}, {ingredient.measurement_unit}'
        expected_recipe_name = recipe.name

        self.assertEqual(expected_tag_name, str(tag))
        self.assertEqual(expected_ingredient_name, str(ingredient))
        self.assertEqual(expected_recipe_name, str(recipe))
