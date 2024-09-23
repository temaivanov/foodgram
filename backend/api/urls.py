from django.urls import include, path
from rest_framework import routers

from api.views import (
    UserViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet
)

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


# Подключаем роутеры в схему сайта:
# api/{router} -- все остальные маршруты.
# api/auth/token/login/ (Djoser Token Based Authentication)
# api/auth/token/logout/ (Djoser Token Based Authentication)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),  # токены
]
