"""Вьюсеты для работы с отзывами и комментариями."""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.db import models

from content.models import Title
from reviews.models import Review, Comment
from api.permissions import IsAdminAuthorModeratorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_title(self) -> Title:
        """Получение произведения по ID."""
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def update_rating(self, title) -> None:
        """Обновление рейтинга произведения."""
        reviews = title.reviews.all()
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            title.rating = round(total_score / reviews.count(), 2)
        else:
            title.rating = None
        title.save()

    def get_queryset(self) -> models.QuerySet[Review]:
        """Возвращает все отзывы произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer) -> None:
        """Переопределение метода добавления отзыва.

        Проверка уникальности. Обновлением рейтинга.
        """
        if Review.objects.filter(
            title=self.get_title(), author=self.request.user
        ).exists():
            raise ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
        serializer.save(author=self.request.user, title=self.get_title())
        self.update_rating(title=self.get_title())

    def perform_update(self, serializer) -> None:
        """Переопределение метода обновления отзыва с обновлением рейтинга."""
        instance = serializer.save()
        self.update_rating(instance.title)

    def perform_destroy(self, instance) -> None:
        """Переопределение метода удаления отзыва с обновлением рейтинга."""
        title = instance.title
        instance.delete()
        self.update_rating(title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = [IsAdminAuthorModeratorOrReadOnly]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_review(self) -> Review:
        """Получение отзыва по ID."""
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self) -> models.QuerySet[Comment]:
        """Возвращает все комментарии для отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer) -> None:
        """Переопределение метода добавления комментария."""
        serializer.save(author=self.request.user, review=self.get_review())
