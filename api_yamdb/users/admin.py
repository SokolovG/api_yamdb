from django.contrib import admin

from .models import User


@admin.register(User)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'username')