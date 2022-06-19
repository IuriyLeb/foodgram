import rest_framework.permissions
from django.shortcuts import render, get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from .models import Subscribe
from .serializers import UsersListSerializer, UserSubscribeSerializer, CustomUserCreateSerializer
from api.serializers import RecipeMinifiedSerializer
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from api.pagination import DefaultPagination


User = get_user_model()
# Create your views here.


class FoodgramUserViewSet(UserViewSet):
    pagination_class = DefaultPagination
    serializer_class = UserSubscribeSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return (rest_framework.permissions.AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsersListSerializer
        if self.action == 'subscriptions':
            return UserSubscribeSerializer # TODO WTF
        if self.action == 'me':
            return UsersListSerializer
        if self.action == 'create':
            return CustomUserCreateSerializer

    def permission_denied(self, request, **kwargs):
        pass

    @action(
        detail=False,
        methods=['get', 'list'],
        ) # TODO add custom pagination more in docs 'recipes_limit'
    def subscriptions(self, request):
        user = request.user
        subscribitions = User.objects.filter(subscribers__subscribing_user=user)
        page = self.paginate_queryset(subscribitions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            #serializer = UserSubscribeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        #serializer = UserSubscribeSerializer(subscribitions, many=True)
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
    #     serializer = UserMinifiedSerializer(user)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    #
