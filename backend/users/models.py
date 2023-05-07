from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import username_validator


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.MAX_LENGHT_EMAIL, unique=True
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        unique=True,
        max_length=settings.MAX_LENGHT_USERNAME,
        validators=(username_validator,),
    )
    first_name = models.CharField(
        'Имя', max_length=settings.MAX_LENGHT_USERNAME,
    )
    last_name = models.CharField(
        'Фамилия', max_length=settings.MAX_LENGHT_USERNAME,
    )
    password = models.CharField(
        'Пароль', max_length=settings.MAX_LENGHT_PASSWORD,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.author}'
