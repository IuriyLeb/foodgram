from django.shortcuts import render, get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from .models import Subscribe
from api.serializers import RecipeMinifiedSerializer
from api.serializers import UserSubscribeSerializer, UserMinifiedSerializer
from django.contrib.auth import get_user_model


User = get_user_model()
# Create your views here.


class FoodgramUserViewSet(UserViewSet):

    def permission_denied(self, request, **kwargs):
        pass

    @action(
        detail=False,
        methods=['get', 'list'],
        serializer_class=UserSubscribeSerializer)
    def subscribitions(self, request):
        user = request.user
        subscribitions = User.objects.filter(subscribers__subscribing_user=user)
        serializer = self.get_serializer(subscribitions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, id=None):
        if request.method == 'POST':
            user_to_subscribe = get_object_or_404(User, id=id)
            Subscribe.objects.create(
                subscribing_user=request.user,
                user_to_subscribe=user_to_subscribe
            )
            serializer = UserSubscribeSerializer(user_to_subscribe,
                                                 context={'request': request})
            return Response(serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            user_to_subscribe = get_object_or_404(User, id=id)
            Subscribe.objects.filter(
                subscribing_user=request.user,
                user_to_subscribe=user_to_subscribe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(detail=False, methods=['get'])
    # def me(self, request):
    #     user = get_user_model()
    #     serializer = UserSerializer(user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

