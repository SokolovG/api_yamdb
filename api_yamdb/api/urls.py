from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
)
from api.users import (
    SignUpView,
    TokenObtainView,
    UserViewSet
)

router_v1 = routers.DefaultRouter()

router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)


urlpatterns = [
    path('api/v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/',TokenObtainView .as_view()),
]
