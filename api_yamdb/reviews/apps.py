"""Конфигурация приложения для работы с отзывами."""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Конфигурация приложения отзывов."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reviews'
