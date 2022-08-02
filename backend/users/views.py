from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPageNumberPagination
from api.serializers import FollowSerializer

from .mixins import CreateListRetrieveViewSet
from .models import CustomUser, Follow
from .serializers import (ChangePasswordSerializer, CreateCustomUserSerializer,
                          UserSerializer)


class ChangePasswordView(CreateAPIView):
    """Change password view."""

    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                serializer.validated_data.get("current_password")
            ):
                return Response(
                    {_("current_password"): _("Wrong password.")},
                    status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(
                serializer.validated_data.get("new_password"))
            self.object.save()
            return Response(
                {_("message"): _("Password updated successfully")},
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(CreateListRetrieveViewSet):
    """Users view."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return CreateCustomUserSerializer

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        user_instance = self.request.user
        serializer = self.get_serializer(user_instance)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        serializer = FollowSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data, status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated,))
    def subscribe(self, request, pk=None):
        if request.method == 'POST':
            return self.add_obj(Follow, request, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Follow, request, pk)
        return None

    def add_obj(self, model, request, pk):
        author = get_object_or_404(CustomUser, id=pk)
        if model.objects.filter(user=request.user, author=author).exists():
            return Response({
                _('message'): _('Your already has subcribed on this author')
            }, status=status.HTTP_400_BAD_REQUEST)
        if request.user == author:
            return Response({
                _('message'): _("You can't subscribe on yourself")
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = model.objects.create(user=request.user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, model, request, pk):
        author = get_object_or_404(CustomUser, id=pk)
        if request.user == author:
            return Response({
                _('errors'): _("You can't unsubcribed on yourself")
            }, status=status.HTTP_400_BAD_REQUEST)
        obj = model.objects.filter(user=request.user, author=author)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            _('message'):
            _('Subcription on this author has already been deleted')
        }, status=status.HTTP_400_BAD_REQUEST)
