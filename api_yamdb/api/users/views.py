"""Views module for Users.

Contains:
- SignUpView
- TokenObtainView
- UserViewSet
"""
from rest_framework import views, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from api.users.serializers import (
    SignUpSerializer,
    TokenObtainSerializer,
    UserViewSerializer
)
from ..permissions import IsAdminOrForbidden
from users.models import User



class SignUpView(views.APIView):
    """Class for SignUpView for User."""
    permission_classes = [AllowAny]
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
    permission_classes = [AllowAny]
    def post(self, request: Request) -> Response:
        serializer = TokenObtainSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                username = serializer.validated_data.get('username')
                user = User.objects.get(username=username)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {'token': str(refresh.access_token)},
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
    permission_classes = [IsAuthenticated, IsAdminOrForbidden]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    """ViewSet for actions with User model.

    Contains:
    - GET/PATCH/DELETE/POST methods for /users/
    - GET/PATCH for /users/me/
    """

    def get_serializer_context(self):
        return super().get_serializer_context()

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request: Request) -> Response:
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance=user)
            data = serializer.data
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(data=request.data, instance=user, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)