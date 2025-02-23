from rest_framework import filters, viewsets
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from content.filters import TitlesFilter
from content.models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .viewsets import CreateDestroyListViewSet


from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReadOnlyTitleSerializer,
)


class CategoryViewSet(CreateDestroyListViewSet):
    """Вьюсет для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyListViewSet):
    """Вьюсет для жанров"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для произведения"""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ReadOnlyTitleSerializer
        return TitleSerializer
