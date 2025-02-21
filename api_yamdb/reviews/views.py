from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

from content.models import Title
from .models import Review
from .permissions import AuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def update_rating(self, title):
        reviews = title.reviews.all()
        if reviews.exists():
            total_score = sum(review.score for review in reviews)
            title.rating = round(total_score / reviews.count(), 2)
        else:
            title.rating = None
        title.save()

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        if Review.objects.filter(title=self.get_title(), author=self.request.user).exists():
            raise ValidationError('Вы уже оставляли отзыв на это произведение.')
        serializer.save(author=self.request.user, title=self.get_title())
        self.update_rating(title=self.get_title())

    def perform_update(self, serializer):
        instance = serializer.save()
        self.update_rating(instance.title)

    def perform_destroy(self, instance):
        title = instance.title
        instance.delete()
        self.update_rating(title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

