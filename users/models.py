from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    role = models.CharField(
        'Пользовательская роль',
        max_length=16,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
    )
    description = models.TextField(
        'Дополнительная информация',
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    email = models.EmailField('Email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('-id',)
