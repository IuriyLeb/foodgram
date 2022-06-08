from django.test import TestCase
from .models import (Tag, Ingredient, Recipe)


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            author='',
            tags=,
            ingredients=,
            image=,
            cooking_time=
        )