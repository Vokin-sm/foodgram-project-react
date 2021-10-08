from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Component
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    """The Recipe model is needed to create recipe."""
    ingredients = models.ManyToManyField(
        Component,
        related_name='recipe',
        verbose_name='компоненты',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='тег',
    )
    image = models.ImageField(
        'изображение',
        upload_to='recipes/%Y/%m/%d/',
    )
    name = models.CharField(
        'имя',
        max_length=200
    )
    text = models.TextField('текст',)
    cooking_time = models.PositiveIntegerField(
        'время приготовления',
        validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='автор',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    """The ShoppingList model is needed to create shopping list."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='автор',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return self.recipe.name


class Favorites(models.Model):
    """The Favorites model is needed to create favorites list"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='автор',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return self.recipe.name
