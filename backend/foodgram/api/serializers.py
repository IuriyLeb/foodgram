from django.contrib.auth.models import User
from rest_framework import serializers

from users.serializers import UsersListSerializer

from .fields import RecipeImageField
from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


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


class ReadRecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for read the list of recipe's ingredients.
    """

    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class WriteRecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for write the list of recipe's ingredients.
    """

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

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
    Serializer for read the full  information about recipe.
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
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')
        depth = 1


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
        tags_data = validated_data.pop('tags', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
            instance.ingredients.clear()
            instance.tags.clear()
            if tags_data:
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
