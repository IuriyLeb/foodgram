from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )

    color = models.CharField(
        verbose_name='Цвет',
        max_length=50
    )

    slug = models.SlugField()

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100
    )

    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=10
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=20,
        unique=True
    )

    text = models.TextField(
        verbose_name='Описание',
        max_length=300,

    )

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.DO_NOTHING,
        related_name='recipes'
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        through='RecipeTag',
        related_name='recipes'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes'
    )

    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='images'
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_recipes'
    )

    amount = models.FloatField(
        verbose_name='Количество',
    )


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags'
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_recipes'
    )


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
