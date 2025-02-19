from rest_framework import serializers

from .users_validators import email_validator, username_validator
from users.models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[email_validator])
    username = serializers.CharField(validators=[username_validator])

    class Meta:
        model = User
        fields = ['email', 'username']
