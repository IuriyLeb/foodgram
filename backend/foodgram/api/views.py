from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Tag, Ingredient, Recipe, Favorites, ShoppingCart
from .serializers import (TagSerializer, IngredientSerializer,
                          ReadRecipeSerializer, WriteRecipeSerializer)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    #pagination_class = LimitOffsetPagination
    #filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    #filterset_fields = ()
   # search_fields = ()

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user,
    #                     is_favorited=False,
    #                     is_in_shopping_cart=False)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadRecipeSerializer
        return WriteRecipeSerializer
    
    @action(detail=False)
    def download_shopping_cart(self, request):
        pass

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(
                {'id': recipe.id,
                 'name': recipe.name,
                 'image': recipe.image,
                 'cooking_time': recipe.cooking_time},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            ShoppingCart.objects.delete(
                user=request.user,
                recipe=recipe
            )
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            Favorites.objects.create(
                user=request.user,
                recipe=recipe
            )
            return Response(
                {'id': recipe.id,
                 'name': recipe.name,
                 'image': recipe.image,
                 'cooking_time': recipe.cooking_time},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            Favorites.objects.delete(
                user=request.user,
                recipe=recipe
            )
            return Response(status=status.HTTP_204_NO_CONTENT)