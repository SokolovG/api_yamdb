from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

app_name = 'reviews'

reviews_router_v1 = DefaultRouter()
reviews_router_v1.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='title-reviews')
reviews_router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='review-comments')

urlpatterns = [
    path('', include(reviews_router_v1.urls)),
]