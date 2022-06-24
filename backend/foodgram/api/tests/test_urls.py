from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework.test import APIClient

from .test_data import *

User = get_user_model()


class RecipeModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create_user(**test_user_1)
        cls.tag = Tag.objects.create(**test_tag_1)
        cls.ingredient = Ingredient.objects.create(**test_ingredient_1)
        cls.recipe = Recipe.objects.create(
            **test_recipe_1,
            author=RecipeModelTest.user
        )
        cls.recipe.tags.add(RecipeModelTest.tag)
        cls.recipe.ingredients.add(RecipeModelTest.ingredient,
                                   through_defaults={'amount': 10})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=RecipeModelTest.user)

    def test_endpoints_existing_at_desired_location(self):
        """Endpoints exists and available by expected locations."""
        endpoints_prefix = '/api'
        endpoints_names = [
            '/tags/',
            '/recipes/',
            '/ingredients/'
        ]
        for endpoint in endpoints_names:
            endpoint = endpoints_prefix + endpoint
            with self.subTest(endpoint=endpoint):
                response = self.authorized_client.get(endpoint)
                self.assertEqual(response.status_code, HTTPStatus.OK)
