"""Serializer for users API.

Contains:
- SignUpSerializer
- TokenObtainSerializer
- UserViewSerializer
"""
from rest_framework import serializers
from api.users.validators import (
    ConfirmationCodeValidator, username_validator
)
from users.models import User
from users.constants import (
    MAX_EMAIL_LENGTH,
    USERNAME_MAX_LENGTH,
    RESTRICTED_USERNAMES
)
from users.services.verification_service import verification_service
from users.exceptions import (
    CodeGenerateError,
    UsernameEmptyError,
    EmailSendError
)


class SignUpSerializer(serializers.ModelSerializer):
    """SignUpSerializer handles user registration process.

    This serializer validates and creates
    new user accounts with email and username.
    It also handles confirmation code generation and email sending.

    Fields:
        email (EmailField): User's email address
        (max length defined in MAX_EMAIL_LENGTH)
        username (CharField): Unique username
        (max length defined in USERNAME_MAX_LENGTH)

    Validation:
        - Checks if username is not empty or restricted
        - Validates email format
        - Ensures username and email uniqueness
        - Prevents duplicate registrations

    Raises:
        ValidationError:
            - When username is empty or restricted
            - When email/username already exists
            - When email sending fails
            - When confirmation code generation fails
        UsernameEmptyError: When username field is empty
        EmailSendError: When verification email fails to send
        CodeGenerateError: When confirmation code generation fails

    Returns:
        User: Newly created user instance with confirmation code sent to email
    """

    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(validators=[
        username_validator
    ], max_length=USERNAME_MAX_LENGTH)

    def create(self, validated_data) -> User:
        """Create user and triggers email verification process."""
        try:
            self.user = super().create(validated_data)
            confirmation_code = verification_service.generate(
                self.user.username
            )
            verification_service.send_code(self.user.email, confirmation_code)
            print("Email sent")
            return self.user

        except UsernameEmptyError as error:
            raise serializers.ValidationError({
                'username': [error.message]
            })
        except EmailSendError as error:
            if self.user.id:
                self.user.delete()
            raise serializers.ValidationError({
                'email': [error.message]
            })
        except CodeGenerateError:
            raise serializers.ValidationError({
                'non_field_errors':
                    ['Technical error occurred. Please try again later.']
            })

    def validate_username(self, value):
        """Validate user username."""
        if not value:
            raise serializers.ValidationError('Username cannot be empty')

        if value.lower() in RESTRICTED_USERNAMES:
            raise serializers.ValidationError(f'Username cannot be {value}')

        return value

    def validate(self, attrs):
        """Validate other logic."""
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError(
                f'User with mail {email}'
                f' and username {username} already exist',
                code='user_exists'
            )

        if User.objects.filter(
                email=email
        ).exclude(username=username).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists'}
            )

        if User.objects.filter(
                username=username
        ).exclude(email=email).exists():
            raise serializers.ValidationError(
                {'username': 'Username already exists'}
            )

        return attrs

    class Meta:
        """Settings class for User model serialization."""

        model = User
        fields = ['email', 'username']


class TokenObtainSerializer(serializers.Serializer):
    """TokenObtainSerializer handles user authentication via confirmation code.

    This serializer validates the provided username and confirmation code
    for user authentication purposes.

    Fields:
        username (CharField): The username to authenticate
        confirmation_code (CharField):
        The verification code sent to user's email

    Validation:
        - Verifies username exists in database
        - Validates confirmation code format
        - Checks if confirmation code matches for given username

    Raises:
        ValidationError:
            - When username doesn't exist
            - When confirmation code is invalid
            - When code format is incorrect

    Returns:
        dict: Validated data containing username and confirmation code
    """

    username = serializers.CharField(
        validators=[username_validator],
        max_length=USERNAME_MAX_LENGTH
    )
    confirmation_code = serializers.CharField(
        validators=[ConfirmationCodeValidator()]
    )

    def validate_username(self, value):
        """Validate username by exist user."""
        if not User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Username not exist', code='username_not_found'
            )

        return value

    def validate(self, attrs):
        """Validate by checking confirmation code."""
        username = attrs.get('username')
        confirmation_code = attrs.get('confirmation_code')
        if verification_service.check_code(
                code=confirmation_code, username=username
        ):
            return attrs

        raise serializers.ValidationError(
            {'confirmation_code': 'Invalid confirmation code'}
        )


class UserViewSerializer(serializers.ModelSerializer):
    """UserViewSerializer handles user profile data serialization.

    This serializer manages user profile information and role assignments.
    Role field is only writable for admin users.

    Fields:
        username (CharField): User's username
        email (EmailField): User's email address
        first_name (CharField): User's first name
        last_name (CharField): User's last name
        bio (CharField): User's biography
        role (ChoiceField): User's role in system (admin/user/moderator)

    Notes:
        - Role field becomes read-only for non-admin users
        - All fields are optional except username and email
        - Role choices are defined in User.RoleChoices

    Permissions:
        - Only admin users can modify role field
        - All users can view and modify their own profile data
    """

    role = serializers.ChoiceField(
        choices=User.RoleChoices,
        default=User.RoleChoices.USER
    )

    def __init__(self, *args, **kwargs):
        """Check field role for read_only."""
        super().__init__(*args, **kwargs)
        if not self.context['request'].user.is_admin:
            self.fields['role'].read_only = True

    class Meta:
        """Settings class for User model serialization."""

        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
