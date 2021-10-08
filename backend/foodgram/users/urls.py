from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowAddDelete, FollowViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'subscriptions',
    FollowViewSet,
    basename='subscriptions'
)

router_v1.register(
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
        include(router_v1.urls)
    ),
]
