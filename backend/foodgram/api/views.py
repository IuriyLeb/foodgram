import os

from django.conf import settings
from django.db.models import Exists, OuterRef
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorites, Ingredient, Recipe, ShoppingCart, Tag)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilterSet
from .permissions import IsAuthorOrAuth
from .serializers import (IngredientSerializer, ReadRecipeSerializer,
                          TagSerializer, WriteRecipeSerializer)
from .utils import process_shopping_cart, render_pdf

pdfmetrics.registerFont(
    TTFont('VC', os.path.join(settings.BASE_DIR,
                              'static_backend/fonts/VinSlabPro-Light_0.ttf')
           )
)


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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RecipeFilterSet
    ordering = ('-id',)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (AllowAny(),)
        if self.action == 'create':
            return (IsAuthenticated(),)
        if self.action in ['update', 'delete']:
            return (IsAuthorOrAuth(),)
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user.id

        is_favorited = Favorites.objects.filter(
            recipe=OuterRef('pk'),
            user=user
        )

        is_in_shopping_cart = Favorites.objects.filter(
            recipe=OuterRef('pk'),
            user=user
        )

        queryset = Recipe.objects.all().annotate(
            is_favorited=Exists(is_favorited),
            is_in_shopping_cart=Exists(is_in_shopping_cart)
        )

        is_favorited = self.request.query_params.get(
            'is_favorited',
            False
        )

        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart',
            False
        )

        if is_favorited:
            return queryset.filter(favorites__user=user)
        if is_in_shopping_cart:
            return queryset.filter(shopping_cart__user=user)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user.id
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer_dict = {
            'is_favorited': Favorites.objects.filter(user=user,
                                                     recipe=instance),
            'is_in_shopping_cart': ShoppingCart.objects.filter(user=user,
                                                               recipe=instance)
        }

        headers = self.get_success_headers(serializer.data)
        instance_serializer = ReadRecipeSerializer(instance,
                                                   context={
                                                       'request': request
                                                   })
        serializer_dict.update(instance_serializer.data)

        return Response(serializer_dict,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        instance_serializer = ReadRecipeSerializer(
            instance,
            context={'request': request}
        )

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(instance_serializer.data)

    @action(detail=False,
            methods=['get', ],
            permission_classes=[IsAuthenticated, ])
    def download_shopping_cart(self, request):

        user = request.user
        shopping_cart_set = user.shopping_cart.all()
        ingredients_dict = process_shopping_cart(shopping_cart_set)
        result = render_pdf(ingredients_dict)
        return FileResponse(result,
                            as_attachment=True,
                            filename='Список покупок.pdf')

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated, ])
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
            shopping_cart_object = get_object_or_404(ShoppingCart,
                                                     user=request.user,
                                                     recipe=recipe)
            shopping_cart_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated, ])
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
            try:
                favorite_object = Favorites.objects.get(user=request.user,
                                                        recipe=recipe)
            except Favorites.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            favorite_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
