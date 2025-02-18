from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import MAX_EMAIL_LENGTH, MAX_ROLE_LENGTH


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'


    email = models.EmailField(unique=True, max_length=MAX_EMAIL_LENGTH)
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=RoleChoices.choices,
        default=RoleChoices.USER
    )

    @property
    def is_admin(self) -> bool:
        return self.role == self.RoleChoices.ADMIN or self.is_superuser

    @property
    def is_moderator(self) -> bool:
        return self.role == self.RoleChoices.MODERATOR