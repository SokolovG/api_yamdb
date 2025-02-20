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


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[email_validator], max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(validators=[username_validator], max_length=USERNAME_MAX_LENGTH)

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_validator], max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        validators=[ConfirmationCodeValidator()],
        min_length=MAX_CONFIRMATION_CODE_LENGTH,
        max_length=MAX_CONFIRMATION_CODE_LENGTH
    )

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']