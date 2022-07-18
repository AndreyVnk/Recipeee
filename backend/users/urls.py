from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    # path('users/', views.UsersViewSet),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]