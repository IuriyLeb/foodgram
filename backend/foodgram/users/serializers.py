from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from recipes.models import Recipe
from rest_framework import serializers

User = get_user_model()


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
    Available via POST to /api/users/.
    """

    password = serializers.CharField(style={"input_type": "password"},
                                     write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id',
                  'username', 'first_name',
                  'last_name', 'password')


class UsersListSerializer(serializers.ModelSerializer):
    """
    Short presentation of User object for users list.
    """

    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')


class UserSubscribeSerializer(serializers.ModelSerializer):
    """
    Serializer for full User object information.
    """
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=False)
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed',
                  'recipes', 'recipes_count')
        depth = 1

    def get_recipes(self, obj):
        if 'recipes_limit' in self.context['request'].query_params:
            recipes_number = int(self.context['request'].
                                 query_params['recipes_limit'])
            recipes = Recipe.objects.filter(author=obj.id)[:recipes_number]
            serializer = RecipeMinifiedSerializer(recipes, many=True)
            return serializer.data
        recipes = Recipe.objects.filter(author=obj.id)
        serializer = RecipeMinifiedSerializer(recipes, many=True)
        return serializer.data
