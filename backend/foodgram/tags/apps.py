from django.apps import AppConfig


class TagsConfig(AppConfig):
    """Setting up the admin panel of tags."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'
    verbose_name = 'Теги'
