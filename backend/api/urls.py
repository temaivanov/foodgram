from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import routers

from api.views import (
    IngredientViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
    redirect_to_full
)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')


# Подключаем роутеры в схему сайта:
# api/users/set_password -- станадртная вью Djoser
# apu/users/me -- станадртная вью Djoser
# api/{router} -- все остальные маршруты.
# api/s/{short_url_code} -- доступ по короткой ссылке.
# api/auth/token/login/ (Djoser Token Based Authentication)
# api/auth/token/logout/ (Djoser Token Based Authentication)

urlpatterns = [
    path('users/set_password/',
         DjoserUserViewSet.as_view({'post': 'set_password'})),
    path('users/me/',
         DjoserUserViewSet.as_view({'get': 'me'})),
    path('', include(router.urls)),
    path('s/<str:short_url_code>/',
         redirect_to_full,
         name='redirect_to_full'),
    path('auth/', include('djoser.urls.authtoken')),  # токены
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
