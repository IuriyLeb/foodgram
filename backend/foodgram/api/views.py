from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import OuterRef, Exists
import io
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import Tag, Ingredient, Recipe, Favorites, ShoppingCart, RecipeIngredient
from .serializers import (TagSerializer, IngredientSerializer,
                          ReadRecipeSerializer, WriteRecipeSerializer)
from users.models import Subscribe
from .filters import RecipeFilterSet
from .permissions import IsAuthorOrAuth

pdfmetrics.registerFont(TTFont('VC',
                               os.path.join(settings.STATIC_ROOT, 'fonts/VinSlabPro-Light_0.ttf')))


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)




class RecipeViewSet(viewsets.ModelViewSet):
    #queryset = Recipe.objects.all()
    #pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter] #filters.SearchFilter)
    # filterset_fields = ('author__id', 'tags__slug')
    filterset_class = RecipeFilterSet
    ordering = ('-id',)
   # search_fields = ()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (AllowAny(),)
        elif self.action == 'create':
            return (IsAuthenticated(),)
        elif self.action in ['update', 'delete']:
            return (IsAuthorOrAuth(),)
        return super().get_permissions()

    def get_queryset(self):
        if 'is_favorited' in self.request.query_params:
            is_favorited = int(self.request.query_params['is_favorited'])
            if is_favorited:
                user = self.request.user.id
                return Recipe.objects.filter(favorites__user=user)
        if 'is_in_shopping_cart' in self.request.query_params:
            is_in_shopping_cart = int(self.request.query_params['is_in_shopping_cart'])
            if is_in_shopping_cart:
                user = self.request.user.id
                return Recipe.objects.filter(shopping_cart__user=user)
            user = self.request.user.id

            return Recipe.objects.all()
        return Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    def render_pdf(self, ingredients):
        buffer = io.BytesIO()
        pdf_file = canvas.Canvas(buffer, pagesize=A5)
        #pdf_file.translate(180, 30)
        x, y = 30, 550
        pdf_file.setFont('VC', 14)
        textobject = pdf_file.beginText(x, y)
        for ingredient, quantity in ingredients.items():
            result_string = (
                    ingredient + f' ({quantity[1]})' +
                    f' -- ' + f'{quantity[0]}'
            )
            textobject.textLine(result_string)


        pdf_file.drawText(textobject)

        pdf_file.showPage()
        pdf_file.save()
        buffer.seek(0)
        return buffer
    
    @action(detail=False,
            methods=['get',],
            permission_classes=[IsAuthenticated,])
    def download_shopping_cart(self, request):
        ingredients_dict = {}
        user = request.user
        shopping_cart_set = user.shopping_cart.all()
        for shopping_cart in shopping_cart_set:
            recipe = Recipe.objects.get(id=shopping_cart.recipe.id)
            recipes_set = RecipeIngredient.objects.filter(recipe=recipe)
            for recipe in recipes_set:
                print(recipe.ingredient.name, recipe.amount)
                if recipe.ingredient.name not in ingredients_dict.keys():
                    ingredients_dict[recipe.ingredient.name] = [
                        recipe.amount,
                        recipe.ingredient.measurement_unit
                    ]
                else:
                    ingredients_dict[recipe.ingredient.name][0] += recipe.amount
        result = self.render_pdf(ingredients_dict)
        return FileResponse(result, as_attachment=True, filename='Список покупок.pdf')
        print(ingredients_dict)



    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated,])
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
                 'image': recipe.image.url,
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

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated,])
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
                 'image': recipe.image.url,
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