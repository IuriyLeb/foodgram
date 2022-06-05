from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodgramUserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    r'users',
    FoodgramUserViewSet,
    basename='user'
)


router = DefaultRouter()
router.register('users', FoodgramUserViewSet)
urlpatterns = [

    # path('', include('djoser.urls')),  # TODO check POST
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
