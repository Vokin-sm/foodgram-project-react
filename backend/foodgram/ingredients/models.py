from django.db import models


class Ingredient(models.Model):
    """The Ingredient model is needed to create ingredient."""
    name = models.CharField(
        'Имя',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
