"""Сериализаторы для моделей отзывов и комментариев."""
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    score = serializers.IntegerField(
        min_value=1,
        max_value=10,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        """Мета-класс для настройки сериализатора отзывов."""

        model = Review
        fields = ("id", "text", "author", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для моделы комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )

    class Meta:
        """Мета-класс для настройки сериализатора комментариев."""

        model = Comment
        fields = ("id", "text", "author", "pub_date")
