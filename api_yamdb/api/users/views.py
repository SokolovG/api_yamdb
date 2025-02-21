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
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.users.serializers import (
    SignUpSerializer,
    TokenObtainSerializer,
    UserViewSerializer
)
from users.models import User
from users.services.verification_service import verification_service
from users.exceptions import (CodeExpiredError)



class SignUpView(views.APIView):
    """Class for SignUpView for User."""

    def post(self, request: Request) -> Response:
        serializer = SignUpSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as error:
            if error.get_codes().get('non_field_errors') == ['user_exists']:
                return Response(status=status.HTTP_200_OK)
            raise

        serializer.save()
        data = serializer.data
        return Response(
            {
                'email': data['email'],
                'username': data['username']
            },
            status=status.HTTP_200_OK
        )


class TokenObtainView(views.APIView):
    """CLass for issuance of token to the user."""
    def post(self, request: Request) -> Response:
        serializer = TokenObtainSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                username = serializer.validated_data.get('username')
                user = User.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {'token': str(refresh)},
                    status=status.HTTP_200_OK
                )

        except ValidationError as error:
            if error.get_codes().get('username') == ['username_not_found']:
                return Response(status=status.HTTP_404_NOT_FOUND)
            raise

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    lookup_field = 'username'

    """ViewSet for actions with User model.

    Contains:
    - GET/PATCH/DELETE/POST methods for /users/
    - GET/PATCH for /users/me/
    """

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request: Request) -> Response:
        user = request.user
        if request.method == 'GET':
            serializer = self.serializer_class(instance=user)
            data = serializer.data
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.serializer_class(data=request.data, instance=user)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)