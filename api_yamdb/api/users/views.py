"""Views module for Users.

Contains:
- SignUpView
- TokenObtainView
- UserViewSet
"""
from rest_framework import views
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from http import HTTPStatus

from api.users.serializers import (
    SignUpSerializer,
    TokenObtainSerializer,
    UserViewSerializer
)
from users.models import User
from users.services.verification_service import verification_service
from users.exceptions import (
    EmailEmptyError,
    CodeGenerateError,
    SMTPException,
    CodeExpiredError
)



class SignUpView(views.APIView):
    """Class for SignUpView for User."""
    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get('email')
            username = validated_data.get('username')
            try:
                confirmation_code = verification_service.generate(username)
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
    def post(self, request: Request) -> Response:
        serializer = TokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            username = validated_data.get('username')
            email = validated_data.get('email')
            confirmation_code = validated_data.get('confirmation_code')
            try:
                if verification_service.check_code(code=confirmation_code, username=username):
                    return Response(status=HTTPStatus.OK)
            except CodeExpiredError:
                return Response(
                    {'email': ['Failed to confirm code']},
                    status=HTTPStatus.BAD_REQUEST
                )

        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    """ViewSet for actions with User model.

    Contains:
    - GET/PATCH/DELETE/POST methods for /users/
    - GET/PATCH for /users/me/
    """

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request: Request) -> Response:
        return Response