from django import views
from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, ChangePasswordView

app_name = 'users'

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('users/set_password/', ChangePasswordView.as_view(), name='change-password'),
    #path('auth/', include('rest_auth.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
]