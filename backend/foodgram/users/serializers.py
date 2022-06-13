from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers, pagination
from .models import Subscribe
from django.contrib.auth.models import User, AnonymousUser
from api.models import Recipe

User = get_user_model()


# class PaginatedRecipeMinifiedSerializer(pagination.Pagi):
#     """
#     Short presentation of Recipe object for list of user's recipes.
#     """
#
#     class Meta:
#         ob

class RecipeMinifiedSerializer(serializers.ModelSerializer):
    """
    Short representation of Recipe object for list of user's recipes.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Custom serializer for create user.
    """

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class UsersListSerializer(serializers.ModelSerializer):
    """
    Short presentation of User object for users list.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if self.context['request'].user == AnonymousUser or obj == AnonymousUser:
            return False
        return Subscribe.objects.filter(
            subscribing_user=self.context['request'].user,
            user_to_subscribe=obj.id # TODO
        ).exists()


class UserSubscribeSerializer(serializers.ModelSerializer):
    """
    Serializer for full User object information.
    """
    recipes = serializers.SerializerMethodField()
    #recipes = PaginatedRecipeMinifiedSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')
        depth = 1

    def get_recipes(self, obj):
        if 'recipes_limit' in self.context['request'].query_params:
            recipes_number = int(self.context['request'].query_params['recipes_limit'])
            recipes = Recipe.objects.filter(author=obj.id)[:recipes_number]
            serializer = RecipeMinifiedSerializer(recipes, many=True)
            return serializer.data
            print(obj)
        else:
            recipes = Recipe.objects.filter(author=obj.id)
            serializer = RecipeMinifiedSerializer(recipes, many=True)
            return serializer.data
        pass



    def get_is_subscribed(self, obj):
        if self.context['request'].user == AnonymousUser or obj == AnonymousUser:
            return False
        print(self.context['request'].query_params)
        print()
        if 'recipes_limit' in self.context['request'].query_params:
            print('Юрий вы победитель')
        return Subscribe.objects.filter(
            subscribing_user=self.context['request'].user,
            user_to_subscribe=obj.id
        ).exists()

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.id).count()

class UserMinifiedSerializer(serializers.ModelSerializer): # TODO rename to RecipeAuthorSerializer
    """
    Short presentation of User object for recipe's author.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        print('!!!!!!!!!!', obj, self.context['request'].user)
        if self.context['request'].user == AnonymousUser or obj == AnonymousUser:
            return False
        return Subscribe.objects.filter(
            subscribing_user=self.context['request'].user,
            user_to_subscribe=obj.id # TODO
        ).exists()


class SubscribeSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = Subscribe
        fields = ()