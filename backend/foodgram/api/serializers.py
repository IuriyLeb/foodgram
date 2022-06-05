from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


from users.models import Subscribe
from .fields import RecipeImageField


from .models import (Tag, Recipe, RecipeIngredient, RecipeTag,
                     Ingredient, Favorites, ShoppingCart) 

class RecipeMinifiedSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_subscribed'
                    )

    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(subscribing_user=self.context['request'].user,
                                         user_to_subscribe=obj.id).exists() 


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ()

class UserSubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeMinifiedSerializer(many=True)
    recipes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed', 
                  'recipes', 'recipes_count'
                    )
        depth = 1
    
    def get_is_subscribed(self, obj):
        return Subscribe.objects.filter(subscribing_user=self.context['request'].user,
                                         user_to_subscribe=obj.id).exists()   
        
    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.id).count()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    ingredient = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')       
  
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'ingredient', 'measurement_unit', 'amount')


class RecipeTagSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='tag.id')
    name = serializers.ReadOnlyField(source='tag.name')
    color = serializers.ReadOnlyField(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug')


class ReadRecipeSerializer(serializers.ModelSerializer):
    tags = RecipeTagSerializer(source='recipetag_set', many=True)
    author = UserSerializer(many=False)
    ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')
        depth = 1

    def get_is_favorited(self, obj):
        return Favorites.objects.filter(user=self.context['request'].user,
                                        recipe=obj.id).exists() 
    
    def get_is_in_shopping_cart(self, obj):
        return ShoppingCart.objects.filter(user=self.context['request'].user,
                                        recipe=obj.id).exists()

class WriteRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    
    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

class WriteRecipeSerializer(serializers.ModelSerializer):
    ingredients = WriteRecipeIngredientSerializer(many=True)
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
        
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients_data:
            RecipeIngredient.objects.create(recipe=recipe,
                                                ingredient=ingredient['id'],
                                                amount=ingredient['amount'])
        for tag in tags_data:
            RecipeTag.objects.create(recipe=recipe, tag=tag)
        return super().create(validated_data)

        
        