from rest_framework import serializers

from api.users.validators import (
    email_validator,
    username_validator,
    ConfirmationCodeValidator
)
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[email_validator])
    username = serializers.CharField(validators=[username_validator])

    class Meta:
        model = User
        fields = ['email', 'username']


class TokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[username_validator])
    confirmation_code = serializers.CharField(
        validators=[ConfirmationCodeValidator()]
    )

    class Meta:
        model = User
        fields = ['username', 'confirmation_code']