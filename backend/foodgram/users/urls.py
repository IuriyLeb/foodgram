from django.urls import path, include
from .views import FoodgramUserViewSet

urlpatterns = [

    # path('', include('djoser.urls')),  # TODO check POST
    path('users/', FoodgramUserViewSet.as_view({'get': 'list'})),
    path('auth/', include('djoser.urls.jwt')),
]
