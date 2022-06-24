
import tempfile
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework.test import APIClient

User = get_user_model()

class UrlsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')

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
            author=UrlsModelTest.user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            cooking_time=10
        )
        cls.recipe.tags.add(UrlsModelTest.tag)
        cls.recipe.ingredients.add(UrlsModelTest.ingredient,
                                   through_defaults={'amount': 10})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=UrlsModelTest.user)


    def test_endpoints_existing_at_desired_location(self):
        """Endpoints exists and available by expected locations."""
        endpoints_prefix = '/api'
        endpoints_names = [
            '/users/',
            '/users/me/',
        ]
        for endpoint in endpoints_names:
            endpoint = endpoints_prefix + endpoint
            with self.subTest(endpoint=endpoint):
                response = self.authorized_client.get(endpoint)
                self.assertEqual(response.status_code, HTTPStatus.OK)