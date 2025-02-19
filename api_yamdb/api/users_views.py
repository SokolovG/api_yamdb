"""Views module for Users.

Contains:
- SignUpView
- TokenObtainView
- UserViewSet
"""

from typing import TYPE_CHECKING
from rest_framework import views
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.response import Response


class SignUpView(views.APIView):
    """CLass for SignUpView for User."""


class TokenObtainView(views.APIView):
    """CLass for issuance of token to the user."""

class UserViewSet(ModelViewSet):
    """ViewSet for actions with User model.

    Contains:
    - GET/PATCH/DELETE/POST methods for /users/
    - GET/PATCH for /users/me/
    """

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request: Request) -> Response:
        pass