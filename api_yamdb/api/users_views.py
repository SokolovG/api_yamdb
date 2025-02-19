"""Views module for Users.

Contains:
- SignUpView
- TokenObtainView
- UserViewSet
"""

from typing import TYPE_CHECKING
from rest_framework import views
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from http import HTTPStatus

from users_serializer import SignUpSerializer
from users.services.verification_service import verification_service
from users.exceptions import (
    EmailEmptyError,
    CodeGenerateError,
    SMTPException
)

if TYPE_CHECKING:
    from rest_framework.request import Request


class SignUpView(views.APIView):
    """CLass for SignUpView for User."""
    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get('email')
            try:
                confirmation_code = verification_service.generate(email)
                verification_service.send_code(email, confirmation_code)
                return Response(status=HTTPStatus.OK)

            except (CodeGenerateError, EmailEmptyError, SMTPException):
                return Response(
                    {'email': ['Failed to send confirmation code']},
                    status=HTTPStatus.BAD_REQUEST
                )

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

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
        return Response