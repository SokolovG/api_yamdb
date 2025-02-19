from rest_framework.validators import UniqueValidator, ValidationError

from users.models import User
from users.constants import (
    EMAIL_NOT_UNIQUE_MSG,
    USERNAME_NOT_UNIQUE_MSG,
    MAX_CONFIRMATION_CODE_LENGTH
)



email_validator = UniqueValidator(
    queryset=User.objects.all().only('email'),
    message=EMAIL_NOT_UNIQUE_MSG,
    lookup='iexact'
)

username_validator = UniqueValidator(
    queryset=User.objects.all().only('username'),
    message=USERNAME_NOT_UNIQUE_MSG,
    lookup='iexact'
)


class ConfirmationCodeValidator:
    def __init__(self, length: int = MAX_CONFIRMATION_CODE_LENGTH) -> None:
        self.length = length

    def __call__(self, code: str) -> None:
        if not code.isdigit():
            raise ValidationError('The code must contain only numbers.')

        if len(code) != self.length:
            raise ValidationError(f'The length of the code should be {self.length} numbers.')

