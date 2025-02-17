from django.db import models


from .constant import (
    GENRE_NAME_MAX_LENGTH,
    GENRE_SLUG_MAX_LENGTH,
    CATEGORY_NAME_MAX_LENGTH,
    CATEGORY_SLUG_MAX_LENGTH,
    TITLE_NAME_MAX_LENGTH
)


class Categories(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=CATEGORY_NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        'Код',
        max_length=CATEGORY_SLUG_MAX_LENGTH
    )


class Genres(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=GENRE_NAME_MAX_LENGTH
    )
    slug = models.SlugField(
        'Код',
        max_length=GENRE_SLUG_MAX_LENGTH
    )


class Titles(models.Model):
    name = models.CharField(
        'Наименование',
        max_length=TITLE_NAME_MAX_LENGTH
    )
    year = models.PositiveSmallIntegerField(
        'Год выхода',
        min=1900,
        max=2025
    )
    category = models.ForeignKey(
        Categories,
        verbose_name='Категория',
        on_delete=models.CASCADE
    )
