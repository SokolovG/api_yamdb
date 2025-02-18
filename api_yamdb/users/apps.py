"""Classic django app config."""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Default user config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
