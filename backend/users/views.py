from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken
# from reviews.models import Category, Comment, Genre, Review, Title
from .models import CustomUser

from .serializers import (
    CreateCustomUserSerializer,
    UserSerializer,
)

class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass

class UsersViewSet(CreateListRetrieveViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        return CreateCustomUserSerializer 

    #def create(self, request, *args, **kwargs):
    #    serializer = CreateCustomUserSerializer(data=request.data)
    #    if serializer.is_valid(raise_exception=True):
    #        serializer.save()
    #    return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    
    #def perform_create(self, serializer):
    #    serializer.save()

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="users_me",
    )
    def me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status.HTTP_200_OK)
