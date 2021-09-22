from backend.foodgram.ingredients.models import Ingredient
from backend.foodgram.tags.models import Tag
from backend.foodgram.users.models import User
from django.db import models


class Recipe(models.Model):
    """The Recipe model is needed to create recipe."""
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.FileField(upload_to='recipes')
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe'
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
