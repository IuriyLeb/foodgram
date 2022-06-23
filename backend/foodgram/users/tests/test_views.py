import tempfile
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.models import Ingredient, Recipe, RecipeIngredient, Tag

User = get_user_model()

class UrlsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user_1 = User.objects.create_user(email='test@test.com',
                                            username='test',
                                            first_name='Test',
                                            last_name='One')

        cls.test_user_2 = User.objects.create_user(email='test2@test.com',
                                                   username='test2',
                                                   first_name='Test',
                                                   last_name='Two')

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
            author=UrlsModelTest.test_user_1,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            cooking_time=10
        )
        cls.recipe.tags.add(UrlsModelTest.tag)
        cls.recipe.ingredients.add(UrlsModelTest.ingredient,
                                   through_defaults={'amount': 10})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=UrlsModelTest.test_user_1)

    def test_create_user(self):
        number_of_users = User.objects.all().count()
        response = self.guest_client.post('/api/users/',
                               {
                                   "email": "vpupkin@yandex.ru",
                                   "username": "vasya.pupkin",
                                   "first_name": "Вася",
                                   "last_name": "Пупкин",
                                   "password": "1QwErTy123"
                               },
                                          format='json')
        #self.assertEqual(response.status_code, HTTPStatus.CREATED)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(User.objects.all().count(), number_of_users+1)
        self.assertEqual(response.data,
                         {
                             "email": "vpupkin@yandex.ru",
                             "username": "vasya.pupkin",
                             "id": 3,
                             "first_name": "Вася",
                             "last_name": "Пупкин",
                         })


    def test_user_get_token(self):
        self.guest_client.post('/api/users/',
                                          {
                                              "email": "vpupkin@yandex.ru",
                                              "username": "vasya.pupkin",
                                              "first_name": "Вася",
                                              "last_name": "Пупкин",
                                              "password": "1QwErTy123"
                                          },
                                          format='json')
        response = self.guest_client.post('/api/auth/token/login/',
                                          {
                                              "password": "1QwErTy123",
                                              "email": "vpupkin@yandex.ru",

                                          },
                                          format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        token = response.data['auth_token']

        self.guest_client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.guest_client.get('/api/users/me/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


