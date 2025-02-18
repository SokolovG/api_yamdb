"""Django admin panel settings."""
from django.contrib import admin

from .models import User


@admin.register(User)
class ModelNameAdmin(admin.ModelAdmin):
    """Basic admin class for model User."""

    list_display = ('email', 'role', 'username')
