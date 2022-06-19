from rest_framework import serializers
from django.contrib.auth.models import User, AnonymousUser

from users.models import Subscribe
from users.serializers import UserMinifiedSerializer, UsersListSerializer
from .fields import RecipeImageField
from .models import (Tag, Recipe, RecipeIngredient, RecipeTag,
                     Ingredient, Favorites, ShoppingCart)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag objects.
    """

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for Ingredient objects.
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """
    Short representation of Recipe object for list of user's recipes.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ReadRecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for read the list of recipe's ingredients.
    """

    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'measurement_unit', 'amount')


class WriteRecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for write the list of recipe's ingredients.
    """

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeTagSerializer(serializers.ModelSerializer):
    """
    Serializer for read the list of recipe's tags.
    """

    id = serializers.ReadOnlyField(source='tag.id')
    name = serializers.ReadOnlyField(source='tag.name')
    color = serializers.ReadOnlyField(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for read the recipe's information.
    """

    author = UsersListSerializer(many=False)
    tags = RecipeTagSerializer(
        source='recipe_tags',
        many=True
    )
    ingredients = ReadRecipeIngredientSerializer(
        source='recipe_ingredients',
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')
        depth = 1

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Favorites.objects.filter(
            user=self.context['request'].user,
            recipe=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=self.context['request'].user,
            recipe=obj.id
        ).exists()


class WriteRecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for create recipe.
    """

    ingredients = WriteRecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients',

    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = RecipeImageField()

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients',
                  'image', 'name', 'text', 'cooking_time')
        depth = 1

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

        for tag in tags_data:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipe_ingredients')
        tags_data = validated_data.pop('tags', None)  # TODO check tags can be empty

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.ingredients.clear()
            instance.tags.clear()
            if tags_data is not None:
                for tag in tags_data:
                    RecipeTag.objects.create(recipe=instance, tag=tag)
            for ingredient in ingredients_data:
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
            instance.save()
        return instance
