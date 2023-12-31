from django.db import models
from django.contrib.auth.models import AbstractUser

from users.validators import validate_username


class User(AbstractUser):
    email = models.EmailField(unique=True,
                              validators=[validate_username],
                              verbose_name='Почта')
    first_name = models.CharField(max_length=200, verbose_name='Фамилия')
    last_name = models.CharField(max_length=200, verbose_name='Имя')

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор'
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
