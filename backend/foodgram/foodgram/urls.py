from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/users/', include('users.urls')),
    path('api/tags/', include('tags.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/ingredients/', include('ingredients.urls')),
]
