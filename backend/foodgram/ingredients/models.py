from django.db import models


class Ingredient(models.Model):
    """The Ingredient model is needed to create ingredient."""
    name = models.CharField(
        'Имя',
        max_length=200,
        blank=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        blank=True,
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
    amount = models.PositiveIntegerField(
        'количество',
        blank=True,
    )

    class Meta:
        verbose_name = 'Компонент'
        verbose_name_plural = 'Компоненты'

    def __str__(self):
        return f'{self.name}/{self.amount}'
