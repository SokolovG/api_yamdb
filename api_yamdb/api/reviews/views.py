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

    def get_queryset(self) -> models.QuerySet[Review]:
        """Возвращает все отзывы произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer) -> None:
        """Переопределение метода добавления отзыва.

        Проверка уникальности.
        """
        title = self.get_title()
        if title.reviews.filter(author=self.request.user).exists():
            raise ValidationError(
                "Вы уже оставляли отзыв на это произведение."
            )
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer) -> None:
        """Переопределение метода обновления отзыва."""
        serializer.save()

    def perform_destroy(self, instance) -> None:
        """Переопределение метода удаления отзыва."""
        instance.delete()


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
        return self.get_review().comments.all().order_by('-pub_date')

    def perform_create(self, serializer) -> None:
        """Переопределение метода добавления комментария."""
        serializer.save(author=self.request.user, review=self.get_review())
