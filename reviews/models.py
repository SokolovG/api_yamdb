from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from users.midels import Title

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
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        # Строка формата 'автор - произведение'.
        return f'{self.author} - {self.title}'

class Comment(models.Model):
    """Модель комментария к отзыву.

    Атрибуты:
        review (ForeignKey): Ссылка на отзыв, к которому относится комментарий.
        text (TextField): Текст комментария.
        author (ForeignKey): Ссылка на автора комментария (пользователя).
        pub_date (DateTimeField): Дата и время создания комментария.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        # Строка формата 'автор - отзыв'
        return f'{self.author} - {self.review}'
