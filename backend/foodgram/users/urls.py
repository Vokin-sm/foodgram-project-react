from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users import views

router = DefaultRouter()
router.register('', views.CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
