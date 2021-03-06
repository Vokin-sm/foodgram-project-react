from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model."""
    email = models.EmailField(
        'почта',
        unique=True,
    )
    first_name = models.CharField(
        'имя',
        max_length=150
    )
    last_name = models.CharField(
        'фамилия',
        max_length=150
    )


class Follow(models.Model):
    """The Follow model is needed to create subscribers."""
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Подписчик'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user}/{self.author}'
