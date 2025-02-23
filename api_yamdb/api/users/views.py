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


class PublicAPIView(views.APIView):
    """Base class for public API endpoints.

    This view is accessible without authentication.

    Attributes:
        permission_classes: List containing AllowAny permission class
        authentication_classes: Empty list to disable authentication
    """

    permission_classes = [AllowAny]
    authentication_classes = []


class SignUpView(PublicAPIView):
    """Handle user registration process.

    This view processes new user registrations by validating provided
    email and username, creating new user accounts, and triggering
    email verification.

    Endpoints:
        POST /signup/: Create new user account

    Permissions:
        - AllowAny: Endpoint is public

    Returns:
        Response with status 200 and user data on success
        Response with status 200 if user already exists
        Response with validation errors otherwise
    """

    def post(self, request: Request) -> Response:
        """Process user registration request.

        Args:
            request (Request): HTTP request containing user data
                Required fields:
                - email: User's email address
                - username: Desired username

        Returns:
            Response: JSON response containing:
                - email: Registered email
                - username: Registered username
            Status codes:
                200: Registration successful or user exists
                400: Validation errors
        """
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


class TokenObtainView(PublicAPIView):
    """Handle JWT token generation for user authentication.

    This view validates user credentials via confirmation code
    and generates JWT tokens for authenticated sessions.

    Endpoints:
        POST /token/: Generate JWT token

    Permissions:
        - AllowAny: Endpoint is public

    Returns:
        Response with JWT token on success
        Response with error details on failure
    """

    def post(self, request: Request) -> Response:
        """Process token generation request.

        Args:
            request (Request): HTTP request containing authentication data
                Required fields:
                - username: User's username
                - confirmation_code: Verification code from email

        Returns:
            Response: JSON containing:
                - token: JWT access token
            Status codes:
                200: Token generated successfully
                404: Username not found
                400: Invalid confirmation code or validation errors
        """
        serializer = TokenObtainSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
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


class UserViewSet(ModelViewSet):
    """ViewSet for managing user accounts and profiles.

    This ViewSet provides CRUD operations for user management
    and includes a special endpoint for managing own profile.

    Endpoints:
        - GET /users/: List all users (admin only)
        - POST /users/: Create new user (admin only)
        - GET /users/{username}/: Retrieve specific user
        - PATCH /users/{username}/: Update specific user
        - DELETE /users/{username}/: Delete specific user
        - GET/PATCH /users/me/: Manage own profile

    Permissions:
        - IsAuthenticated: Basic access
        - IsAdminOrForbidden: Admin-only operations

    Filters:
        - Search: Filter users by username
    """

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
        """Get default serializer context with request, view and format."""
        return super().get_serializer_context()

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request: Request) -> Response:
        """Handle current user profile operations.

        Args:
           request (Request): HTTP request object.
               GET: Retrieve user profile
               PATCH: Update profile fields

        Returns:
           Response: JSON with profile data
           Status codes:
               200: Success
               400: Validation errors on update
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(instance=user)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                data=request.data,
                instance=user,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
