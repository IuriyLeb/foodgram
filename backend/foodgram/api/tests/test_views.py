from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework.test import APIClient

from .test_data import *

User = get_user_model()


class TagViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tag_1 = Tag.objects.create(**test_tag_1)
        cls.tag_2 = Tag.objects.create(**test_tag_2)

        test_tag_1.update({'id': TagViewSetTest.tag_1.id})
        test_tag_2.update({'id': TagViewSetTest.tag_2.id})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()

    def test_get_tags_list(self):

        response = self.guest_client.get('/api/tags/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(test_tag_1, response.data)
        self.assertIn(test_tag_2, response.data)

    def test_tag_detail(self):
        response = self.authorized_client.get('/api/tags/1/') # TODO hide all variables

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, test_tag_1)


class IngredientViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ingredient_1 = Ingredient.objects.create(**test_ingredient_1)
        cls.ingredient_2 = Ingredient.objects.create(**test_ingredient_2)

        test_ingredient_1.update({'id': IngredientViewSetTest.ingredient_1.id})
        test_ingredient_2.update({'id': IngredientViewSetTest.ingredient_2.id})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()

    def test_get_ingredients_list(self):

        response = self.guest_client.get('/api/ingredients/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(test_ingredient_1 in response.data)
        self.assertTrue(test_ingredient_2 in response.data)

    def test_ingredient_detail(self):
        response = self.guest_client.get('/api/ingredients/1/') # TODO hide all variables

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, test_ingredient_1)


class RecipeViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(**test_user_1)

        cls.tag_1 = Tag.objects.create(**test_tag_1)
        cls.tag_2 = Tag.objects.create(**test_tag_2)

        test_tag_1.update({'id': RecipeViewSetTest.tag_1.id})
        test_tag_2.update({'id': RecipeViewSetTest.tag_2.id})

        cls.ingredient_1 = Ingredient.objects.create(**test_ingredient_1)
        cls.ingredient_2 = Ingredient.objects.create(**test_ingredient_2)

        test_ingredient_1.update({'id': RecipeViewSetTest.ingredient_1.id})
        test_ingredient_2.update({'id': RecipeViewSetTest.ingredient_2.id})

        cls.recipe_1 = Recipe.objects.create(**test_recipe_1,
                                             author=RecipeViewSetTest.user)

        cls.recipe_1.tags.add(RecipeViewSetTest.tag_1)
        cls.recipe_1.ingredients.add(RecipeViewSetTest.ingredient_1,
                                     through_defaults={'amount': 10})

        test_recipe_1.update({'id': RecipeViewSetTest.recipe_1.id})

        cls.recipe_2 = Recipe.objects.create(**test_recipe_2,
                                             author=RecipeViewSetTest.user)

        cls.recipe_1.tags.add(RecipeViewSetTest.tag_2)
        cls.recipe_1.ingredients.add(RecipeViewSetTest.ingredient_2,
                                     through_defaults={'amount': 20})

        test_recipe_2.update({'id': RecipeViewSetTest.recipe_2.id})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=RecipeViewSetTest.user)

    def test_get_recipe_detail(self):
        response = self.authorized_client.get(
            f"/api/recipes/{test_recipe_1['id']}/"
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data['id'], test_recipe_1['id'])
        self.assertEqual(response.data['name'], test_recipe_1['name'])
        self.assertEqual(response.data['text'], test_recipe_1['text'])
        self.assertEqual(response.data['cooking_time'],
                         test_recipe_1['cooking_time'])

    def test_create_recipe(self):
        number_of_recipes = Recipe.objects.all().count()
        response = self.authorized_client.post('/api/recipes/',
                                               test_create_recipe_1,
                                               format='json')

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Recipe.objects.all().count(), number_of_recipes+1)
        self.assertTrue('name' in response.data)
        self.assertEqual(response.data['name'], test_create_recipe_1['name'])

    def test_update_recipe(self):
        self.authorized_client.patch(f"/api/recipes/{test_recipe_1['id']}/",
                                     test_create_recipe_2,
                                     format='json')

        response = self.authorized_client.get(
            f"/api/recipes/{test_recipe_1['id']}/"
        )

        self.assertEqual(response.data['name'], test_create_recipe_2['name'])

    def test_delete_recipe(self):
        number_of_recipes = Recipe.objects.all().count()
        response = self.authorized_client.delete(
            f"/api/recipes/{test_recipe_1['id']}/"
        )
        self.assertEqual(Recipe.objects.all().count(), number_of_recipes-1)
