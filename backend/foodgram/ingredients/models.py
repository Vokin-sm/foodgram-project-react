from django.db import models


class Ingredient(models.Model):
    """The Ingredient model is needed to create ingredient."""
    name = models.CharField(
        'Имя',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Component(models.Model):
    """The Component model is needed to create Component."""
    name = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='component',
        verbose_name='ингредиент',
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )
    amount = models.PositiveIntegerField('количество')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиента'

    def __str__(self):
        return f'{self.name}/{self.amount}'
