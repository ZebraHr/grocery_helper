from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Абстрактная модель пользователя."""
    email = models.EmailField(
        verbose_name='email address',
        max_length=100,
        unique=True,
    )
    username = models.CharField(max_length=40)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
