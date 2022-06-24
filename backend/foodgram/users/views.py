import rest_framework.permissions
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.pagination import DefaultPagination
from .models import Subscribe
from .serializers import (CustomUserCreateSerializer, UsersListSerializer,
                          UserSubscribeSerializer)

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    pagination_class = DefaultPagination
    serializer_class = UserSubscribeSerializer

    def get_queryset(self):
        if self.action == 'list':
            user = self.request.user.id
            is_subscribed = Subscribe.objects.filter(
                subscribing_user=user,
                user_to_subscribe=OuterRef('id')
            )
            queryset = User.objects.all().annotate(
                is_subscribed=Exists(is_subscribed)
            )
            return queryset
        return super().get_queryset()

    def get_permissions(self):
        if self.action == 'retrieve':
            return (rest_framework.permissions.AllowAny(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsersListSerializer
        if self.action == 'subscriptions':
            return UserSubscribeSerializer
        if self.action == 'me':
            return UsersListSerializer
        if self.action == 'create':
            return CustomUserCreateSerializer
        return super().get_serializer_class()

    # def permission_denied(self, request, **kwargs):
    #     pass

    @action(
        detail=False,
        methods=['get', 'list'],
        )
    def subscriptions(self, request):

        user = request.user

        is_subscribed = Subscribe.objects.filter(
            subscribing_user=user,
            user_to_subscribe=OuterRef('id')
        )
        subscribitions = User.objects.filter(
            subscribers__subscribing_user=user
        )
        subscribitions = subscribitions.annotate(
            is_subscribed=Exists(is_subscribed)
        )
        page = self.paginate_queryset(subscribitions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
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
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            user_to_subscribe = get_object_or_404(User, id=id)
            Subscribe.objects.filter(
                subscribing_user=request.user,
                user_to_subscribe=user_to_subscribe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
