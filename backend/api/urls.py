from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()

router.register(r'recipes', views.RecipeViewSet, basename='recipes')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredients')
router.register(r'tags', views.TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]