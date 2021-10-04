from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import Follow


class CustomUserSerializer(UserSerializer):
    """Is used to serialize users."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]

    def get_is_subscribed(self, obj):
        if self.context['request'].auth:
            current_user = self.context['request'].user
            try:
                Follow.objects.get(author=obj, user=current_user)
            except Follow.DoesNotExist:
                return False
            return True
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    """Is used to serialize users."""
    class Meta(UserCreateSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
