"""Models file.

Contains User model.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

from .constants import (
    MAX_EMAIL_LENGTH,
    MAX_ROLE_LENGTH, MAX_BIO_LENGTH
)


class User(AbstractUser):
    """User model from AbstractUser.

    Added fields:
    - role
    - email is blank=False

    Contains RoleChoices for choices
    """

    class RoleChoices(models.TextChoices):
        """Class choices for field role."""

        USER = 'user', 'User'
        MODERATOR = 'moderator', 'Moderator'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(
        unique=True,
        max_length=MAX_EMAIL_LENGTH,
        blank=False
    )
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=RoleChoices.choices,
        default=RoleChoices.USER
    )
    bio = models.CharField(
        max_length=MAX_BIO_LENGTH,
        blank=True
    )

    @property
    def is_admin(self) -> bool:
        """Return bool if user is admin or superuser."""
        return self.role == self.RoleChoices.ADMIN or self.is_superuser

    @property
    def is_moderator(self) -> bool:
        """Return bool if user is moderator."""
        return self.role == self.RoleChoices.MODERATOR

    class Meta:
        """CLass meta with ordering by username."""

        ordering = ['username']
