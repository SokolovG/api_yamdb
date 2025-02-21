from django.db import models

from .validators import validate_year

from .constants import (
    GENRE_NAME_MAX_LENGTH,
    GENRE_SLUG_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    TITLE_NAME_MAX_LENGTH
)


class Category(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=CATEGORY_NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        'Код',
        max_length=CATEGORY_SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=GENRE_NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        'Код',
        max_length=GENRE_SLUG_MAX_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=TITLE_NAME_MAX_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        'Год выхода',
        validators=[validate_year]
    )
    description = models.TextField(
        'Описание',
        blank=True
    )
    rating = models.PositiveIntegerField(
        'Рейтинг',
        null=True,
        default=None
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        blank=True, null=True,
        on_delete=models.SET_NULL)
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр',
        blank=True, null=True,
        on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Произведение и жанр'
        verbose_name_plural = 'Произведения и жанры'

    def __str__(self):
        return f'{self.title}, жанр <-> {self.genre}'
