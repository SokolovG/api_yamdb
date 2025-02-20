from django.core.validators import RegexValidator
from rest_framework import serializers

from api.users.validators import (
    email_validator,
    username_validator,
    ConfirmationCodeValidator
)
from users.models import User
from users.constants import (
    MAX_EMAIL_LENGTH,
    MAX_CONFIRMATION_CODE_LENGTH,
    USERNAME_MAX_LENGTH
)
from users.services.verification_service import verification_service
from .exceptions import UserNotFoundException, ConfirmationCodeExpired, ConfirmationCodeInvalid


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[email_validator], max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(validators=[
        username_validator,
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
        )
    ], max_length=USERNAME_MAX_LENGTH)

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(validators=[
        username_validator,
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
        )
], max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        validators=[ConfirmationCodeValidator()],
        min_length=MAX_CONFIRMATION_CODE_LENGTH,
        max_length=MAX_CONFIRMATION_CODE_LENGTH
    )

    class Meta:
        fields = ['username', 'confirmation_code']


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'role']