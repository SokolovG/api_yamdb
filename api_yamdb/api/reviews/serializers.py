from rest_framework import serializers

from reviews.models import Comment, Review
from reviews.constants import MIN_SCORE, MAX_SCORE


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field="username"
    )
    score = serializers.IntegerField(
        min_value=MIN_SCORE,
        max_value=MAX_SCORE,
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
