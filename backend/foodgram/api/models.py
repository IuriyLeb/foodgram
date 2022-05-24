from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.TimeField()
    color = models.CharField(max_length=50)
    slug = models.SlugField()


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    measurement_unit = models.CharField(max_length=10)


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='',
        max_length=20,
        unique=True
    )
    text = models.TextField(
        verbose_name='',
        max_length=300,

    )
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    
    image = models.ImageField()
    
    cooking_time = models.TimeField()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)

    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    amount = models.FloatField()


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag,
                            on_delete=models.CASCADE)


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart')

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
