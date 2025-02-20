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
from users.exceptions import (
    EmailEmptyError,
    CodeGenerateError,
    SMTPException,
)
class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(validators=[
        RegexValidator(
            regex=r'^[\w.@+-]+\Z',
        )
    ], max_length=USERNAME_MAX_LENGTH)

    def create(self, validated_data):
        try:
            user = super().create(validated_data)
            confirmation_code = verification_service.generate(user.username)
            verification_service.send_code(user.email, confirmation_code)
            return user

        except (CodeGenerateError, EmailEmptyError, SMTPException) as e:
            raise serializers.ValidationError({
                'email': ['Failed to send confirmation code']
            })

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Username cant be "me"')

        return value

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if User.objects.filter(username=username, email=email).exists():
            raise serializers.ValidationError(
                f'User with mail {email} and username {username} already exist',
                code='user_exists'
            )

        if User.objects.filter(email=email).exclude(username=username).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        if User.objects.filter(username=username).exclude(email=email).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})

        return attrs


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