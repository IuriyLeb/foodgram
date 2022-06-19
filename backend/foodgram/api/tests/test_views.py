from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
import tempfile
from http import HTTPStatus
from api.models import (Tag, Ingredient, Recipe, RecipeIngredient)

User = get_user_model()


class TagViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #cls.user = User.objects.create_user(username='test')

        cls.tag_1 = Tag.objects.create(
            name='Тестовый тег 1',
            color='#FFFFFF',
            slug='test_tag_1'
        )
        cls.tag_2 = Tag.objects.create(
            name='Тестовый тег 2',
            color='#FFFFFF',
            slug='test_tag_2'
        )

        # cls.ingredient = Ingredient.objects.create(
        #     name='Лук',
        #     measurement_unit='шт.'
        # )
        # cls.recipe = Recipe.objects.create(
        #     name='Луковый пирог',
        #     text='Вкуснейший пирог на всем свете',
        #     author=RecipeModelTest.user,
        #     image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        #     cooking_time=10
        # )
        # cls.recipe.tags.add(RecipeModelTest.tag)
        # cls.recipe.ingredients.add(RecipeModelTest.ingredient,
        #                            through_defaults={'amount': 10})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        #self.authorized_client.force_authenticate(user=TagViewSetTest.user)

    def test_get_tags_list(self):

        response = self.guest_client.get('/api/tags/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        #print(response.data) # TODO remove all prints

        self.assertIn({
            'id':1,
            'name':'Тестовый тег 1',
            'color':'#FFFFFF',
            'slug':'test_tag_1'
        }, response.data)
        self.assertIn({
            'id':2,
            'name':'Тестовый тег 2',
            'color':'#FFFFFF',
            'slug':'test_tag_2'
        }, response.data)

    def test_tag_detail(self):
        response = self.authorized_client.get('/api/tags/1/') # TODO hide all variables
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data,
                         {
                             'id':1,
                             'name':'Тестовый тег 1',
                             'color':'#FFFFFF',
                             'slug':'test_tag_1'
                         })


class IngredientViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        #cls.user = User.objects.create_user(username='test')

        cls.ingredient_1 = Ingredient.objects.create(
                 name='Лук',
                 measurement_unit='шт.'
             )
        cls.ingredient_2 = Ingredient.objects.create(
            name='Морковь',
            measurement_unit='кг.'
        )

        # cls.ingredient = Ingredient.objects.create(
        #     name='Лук',
        #     measurement_unit='шт.'
        # )
        # cls.recipe = Recipe.objects.create(
        #     name='Луковый пирог',
        #     text='Вкуснейший пирог на всем свете',
        #     author=RecipeModelTest.user,
        #     image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        #     cooking_time=10
        # )
        # cls.recipe.tags.add(RecipeModelTest.tag)
        # cls.recipe.ingredients.add(RecipeModelTest.ingredient,
        #                            through_defaults={'amount': 10})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        #self.authorized_client.force_authenticate(user=TagViewSetTest.user)

    def test_get_ingredients_list(self):

        response = self.guest_client.get('/api/ingredients/')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        #print(response.data) # TODO remove all prints

        self.assertTrue({
            'id':2,
            'name':'Морковь',
            'measurement_unit':'кг.'
        } in response.data)
        self.assertTrue({
            'id':1,
            'name':'Лук',
            'measurement_unit':'шт.'
        } in response.data)

    def test_ingredient_detail(self):
        response = self.guest_client.get('/api/ingredients/1/') # TODO hide all variables
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data,
                         {
                             'id':1,
                             'name':'Лук',
                             'measurement_unit':'шт.'
                         })

class RecipeViewSetTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')

        cls.tag_1 = Tag.objects.create(
            name='Тестовый тег 1',
            color='#FFFFFF',
            slug='test_tag_1'
        )
        cls.tag_2 = Tag.objects.create(
            name='Тестовый тег 2',
            color='#FFFFFF',
            slug='test_tag_2'
        )

        cls.ingredient_1 = Ingredient.objects.create(
            name='Лук',
            measurement_unit='шт.'
        )
        cls.ingredient_2 = Ingredient.objects.create(
            name='Морковь',
            measurement_unit='кг.'
        )
        cls.recipe_1 = Recipe.objects.create(
            name='Луковый пирог',
            text='Вкуснейший пирог на всем свете',
            author=RecipeViewSetTest.user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            cooking_time=10
        )

        cls.recipe_1.tags.add(RecipeViewSetTest.tag_1)
        cls.recipe_1.ingredients.add(RecipeViewSetTest.ingredient_1,
                                   through_defaults={'amount': 10})
        cls.recipe_2 = Recipe.objects.create(
            name='Морковный пирог',
            text='Лучший морковный',
            author=RecipeViewSetTest.user,
            image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            cooking_time=10
        )
        cls.recipe_1.tags.add(RecipeViewSetTest.tag_2)
        cls.recipe_1.ingredients.add(RecipeViewSetTest.ingredient_2,
                                     through_defaults={'amount': 20})

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=RecipeViewSetTest.user)

    # def test_get_recipes_list(self):
    #
    #     response = self.guest_client.get('/api/recipes/')
    #
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #     print(response.data) # TODO remove all prints
    #
    #     self.assertTrue({
    #         #'id':1,
    #         'name':'Луковый пирог',
    #         # 'color':'#FFFFFF',
    #         # 'slug':'test_tag_1'
    #     } in response.data['results'])
    #     # self.assertTrue({
    #     #     'id':2,
    #     #     'name':'Тестовый тег 2',
    #     #     'color':'#FFFFFF',
    #     #     'slug':'test_tag_2'
    #     # } in response.data)

    def test_get_recipe_detail(self):
        response = self.authorized_client.get('/api/recipes/1/') # TODO hide all variables
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(response.data)
        self.assertEqual(response.data['id'],RecipeViewSetTest.recipe_1.id)
        self.assertEqual(response.data['name'],RecipeViewSetTest.recipe_1.name)
        self.assertEqual(response.data['text'],RecipeViewSetTest.recipe_1.text)
        #self.assertEqual(response.data['author'],RecipeViewSetTest.recipe_1.author)
        #self.assertEqual(response.data['image'],RecipeViewSetTest.recipe_1.image.url)
        self.assertEqual(response.data['cooking_time'],RecipeViewSetTest.recipe_1.cooking_time)

    def test_create_recipe(self):
        number_of_recipes = Recipe.objects.all().count()
        response = self.authorized_client.post('/api/recipes/',
                                          {
                                              'ingredients':[
                                                  {
                                                      'id': 1,
                                                      'amount': 10
                                                  }
                                              ],
                                              'tags':[
                                                  1,2
                                              ],
                                              'image':'"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",',
                                              'name':'Тестовый рецепт',
                                              'text':'Тестовый рецепт',
                                              'cooking_time':5
                                          },
                                          format='json')
        #self.assertEqual(response.status_code, HTTPStatus.CREATED)
        #print(response.data)

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertEqual(Recipe.objects.all().count(), number_of_recipes+1)
        self.assertTrue(

                             'name'
                             # 'text':'Тестовый рецепт',
                             # 'cooking_time':5
                          in response.data)
        self.assertEqual(response.data['name'], 'Тестовый рецепт')


    def test_update_recipe(self):
        self.authorized_client.patch('/api/recipes/1/',
                                                   {
                                                       'ingredients':[
                                                           {
                                                               'id': 1,
                                                               'amount': 10
                                                           }
                                                       ],
                                                       'tags':[
                                                           1,2
                                                       ],
                                                       'image':'"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",',
                                                       'name':'Тестовый рецепт',
                                                       'text':'Тестовый рецепт',
                                                       'cooking_time':5
                                                   },
                                                   format='json')

        response = self.authorized_client.get('/api/recipes/1/')

        self.assertEqual(response.data['name'], 'Тестовый рецепт')


    def test_delete_recipe(self):
        number_of_recipes = Recipe.objects.all().count()
        response = self.authorized_client.delete('/api/recipes/1')
        #self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
        self.assertEqual(User.objects.all().count(), number_of_recipes-1)
