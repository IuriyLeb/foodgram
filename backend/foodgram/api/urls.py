from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import TagViewSet, RecipeViewSet, IngredientViewSet

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
