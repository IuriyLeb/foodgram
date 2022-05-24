from django.shortcuts import render, get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from .models import Subscribe
from api.serializers import RecipeMinifiedSerializer
from api.serializers import UserSubscribeSerializer
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.


class FoodgramUserViewSet(UserViewSet):

    def permission_denied(self, request, **kwargs):
        pass

    @action(detail=False, methods=['list'])
    def subscribitions(self, request):
        pass

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        if request.method == 'POST':
            user_to_subscribe = get_object_or_404(User, id=pk)
            Subscribe.objects.create(
                subscribing_user=request.user,
                user_to_subscribe=user_to_subscribe
            )
            serializer = UserSubscribeSerializer()
            return Response(serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            user_to_subscribe = get_object_or_404(User, id=pk)
            Subscribe.objects.filter(
                subscribing_user=request.user,
                user_to_subscribe=user_to_subscribe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)