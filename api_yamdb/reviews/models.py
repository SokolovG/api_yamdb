from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from content.models import Title
from users.models import User
from .constants import MIN_SCORE, MAX_SCORE


class Review(models.Model):
    """Модель отзыва на произведение.

    Атрибуты:
        title (ForeignKey): произведение, к которому относится отзыв.
        text (TextField): текст отзыва.
        author (ForeignKey): автор отзыва.
        score (IntegerField): оценка от 1 до 10.
        pub_date (DateTimeField): дата и время создания отзыва.
    """

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE),
        ],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        """Мета-класс для настройки модели отзывов."""

        ordering = ("-pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = [
            models.UniqueConstraint(
                fields=("title", "author"), name="unique_review"
            )
        ]

    def __str__(self) -> str:
        """Строка формата 'автор - произведение'."""
        return f"{self.author} - {self.title}"


class Comment(models.Model):
    """Модель комментария к отзыву.

    Атрибуты:
        review (ForeignKey): отзыв, к которому относится комментарий.
        text (TextField): текст комментария.
        author (ForeignKey): автор комментария.
        pub_date (DateTimeField): дата и время создания комментария.
    """

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )

    class Meta:
        """Мета-класс для настройки модели комментариев."""

        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self) -> str:
        """Строка формата 'автор - отзыв'."""
        return f"{self.author} - {self.review}"
