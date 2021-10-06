from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowAddDelete, FollowViewSet

router = DefaultRouter()

router.register(
    'subscriptions',
    FollowViewSet,
    basename='subscriptions'
)

router.register(
    '',
    CustomUserViewSet
)

urlpatterns = [
    path(
        '<int:following_id>/subscribe/',
        FollowAddDelete.as_view(),
        name='subscribe'
    ),
    path(
        '',
        include(router.urls)
    ),
]
