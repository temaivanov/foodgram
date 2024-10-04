from django.contrib import admin
from django.urls import include, path

from api.views import redirect_to_full


# /s/{short_url_code} -- доступ по короткой ссылке.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('s/<str:short_url_code>/',
         redirect_to_full,
         name='redirect_to_full'),
]
