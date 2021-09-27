from djoser.serializers import UserCreateSerializer, UserSerializer


class CustomUserSerializer(UserSerializer):
    """Is used to serialize users."""
    class Meta(UserSerializer.Meta):
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        ]


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
