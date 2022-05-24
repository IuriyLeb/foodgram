from rest_framework.routers import DefaultRouter

from django.urls import path, include



from .views import *

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

    # path('v1/auth/signup/', confirm_email, name='confirm_email'),
    #
    # path('v1/auth/token/', get_token, name='get_token'),

]