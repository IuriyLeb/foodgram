from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(
    r'tags',
    TagViewSet,
    basename='tag'
)

router.register(
    r'recipes',
    RecipeViewSet,
    basename='recipe'
)

router.register(
    r'ingredients',
    IngredientViewSet,
    basename='ingredient'
)


urlpatterns = [
    path('', include(router.urls)),
]
