from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Setting up the admin panel of users."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'
