from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters

from content.models import Category, Genre, Title

from .mixins import CreateDestroyListViewSet

from .permissions import IsAdminOrReadOnly

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)

