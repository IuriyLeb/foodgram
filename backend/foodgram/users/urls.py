from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FoodgramUserViewSet

router = DefaultRouter()
router.register(
    'users',
    FoodgramUserViewSet,
    basename='user'
)

router = DefaultRouter()
router.register('users', FoodgramUserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
