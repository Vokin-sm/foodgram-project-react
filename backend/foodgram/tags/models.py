from django.db import models


class Tag(models.Model):
    """The Tag model is needed to create tag."""
    name = models.CharField(
        'имя',
        max_length=200,
        blank=True,
    )
    color = models.CharField(
        'цвет',
        max_length=7,
        blank=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
